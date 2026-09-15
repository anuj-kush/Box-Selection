import json
import random
from itertools import combinations
from django.test import TestCase, SimpleTestCase, Client
from django.db import IntegrityError, transaction
from .models import Product, Box
from .packing import pack, select_box

def unit(size, pk=1):
    return {'product_id': pk, 'unit': 1, 'size': size}

class PackingTests(SimpleTestCase):
    def test_rotation(self):
        self.assertIsNotNone(pack([unit((8, 2, 3))], (3, 8, 2)))
    def test_volume_is_not_enough(self):
        self.assertIsNone(pack([unit((6, 6, 6)), unit((6, 6, 6), 2)], (10, 10, 10)))
    def test_exact_fit(self):
        self.assertEqual(len(pack([unit((5, 5, 5), i) for i in range(8)], (10, 10, 10))), 8)
    def test_randomized_geometry(self):
        rng = random.Random(42)
        successful = 0
        for _ in range(100):
            units = [unit(tuple(rng.randint(1, 6) for _ in range(3)), i) for i in range(rng.randint(1, 12))]
            placed = pack(units, (10, 10, 10))
            if placed is None:
                continue
            successful += 1
            self.assertEqual(len(placed), len(units))
            self.assertEqual({p['product_id'] for p in placed}, {u['product_id'] for u in units})
            for p in placed:
                self.assertEqual(sorted(p['size_mm']), sorted(units[p['product_id']]['size']))
                self.assertTrue(all(0 <= p['position_mm'][a] and p['position_mm'][a] + p['size_mm'][a] <= 10 for a in range(3)))
            for a, b in combinations(placed, 2):
                self.assertTrue(any(a['position_mm'][k] + a['size_mm'][k] <= b['position_mm'][k] or b['position_mm'][k] + b['size_mm'][k] <= a['position_mm'][k] for k in range(3)))
        self.assertGreater(successful, 20)

class APITests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(name='Cube', length_mm=10, width_mm=10, height_mm=10, weight_g=100)
        self.b = Box.objects.create(name='Box', length_mm=20, width_mm=20, height_mm=20, max_weight_g=200, cost=2)
    def payload(self, qty=1):
        return {'items': [{'product_id': self.p.pk, 'quantity': qty}]}
    def post(self, payload):
        return self.client.post('/api/recommend/', data=json.dumps(payload), content_type='application/json')
    def test_weight_boundary(self):
        self.assertEqual(self.post(self.payload(2)).json()['status'], 'recommended')
        self.assertEqual(self.post(self.payload(3)).json()['checked_boxes'][0]['reason'], 'weight_exceeded')
    def test_cost_and_volume_tie(self):
        cheap = Box.objects.create(name='Cheap', length_mm=30, width_mm=30, height_mm=30, max_weight_g=200, cost=1)
        self.assertEqual(self.post(self.payload()).json()['box']['id'], cheap.pk)
        self.b.cost = 1
        self.b.save()
        self.assertEqual(self.post(self.payload()).json()['box']['id'], self.b.pk)
    def test_inactive(self):
        self.b.active = False
        self.b.save()
        self.assertEqual(self.post(self.payload()).json()['status'], 'no_recommendation')
    def test_unknown(self):
        self.assertEqual(self.post({'items': [{'product_id': 999, 'quantity': 1}]}).status_code, 400)
    def test_invalid(self):
        for data in [None, [], {}, {'items': []}, {'items': 'x'}, {'items': [None]}, self.payload(0), self.payload(-1), self.payload(True), self.payload(1.5), self.payload(51), {'items': [{'product_id': 10**100, 'quantity': 1}]}]:
            with self.subTest(data=data):
                self.assertEqual(self.post(data).status_code, 400)
    def test_duplicates(self):
        data = self.payload()
        data['items'] *= 2
        result = self.post(data).json()
        self.assertEqual(result['total_weight_g'], 200)
        self.assertEqual([p['unit'] for p in result['placements']], [1, 2])
    def test_http_errors(self):
        self.assertEqual(self.client.post('/api/recommend/', data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.post('/api/recommend/', data='x', content_type='text/plain').status_code, 415)
        self.assertEqual(self.client.get('/api/recommend/').status_code, 405)
    def test_page_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertContains(client.get('/'), 'Cube')
        args = dict(data=json.dumps(self.payload()), content_type='application/json')
        self.assertEqual(client.post('/api/recommend/', **args).status_code, 403)
        response = client.post('/api/recommend/', HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value, **args)
        self.assertEqual(response.json()['status'], 'recommended')
    def test_db_constraint(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(name='Bad', length_mm=0, width_mm=1, height_mm=1, weight_g=1)
    def test_dimension_and_volume_rejection(self):
        result = select_box([unit((21, 1, 1))], 1, [self.b])
        self.assertEqual(result['checked_boxes'][0]['reason'], 'item_dimensions_exceeded')
        result = select_box([unit((20, 20, 20)), unit((1, 1, 1), 2)], 1, [self.b])
        self.assertEqual(result['checked_boxes'][0]['reason'], 'volume_exceeded')
