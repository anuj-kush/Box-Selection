- Timestamp (UTC): 2026-09-14T09:43:52.688133+00:00
- Python: 3.12.14
- Django: 5.2.17
- Platform: Linux x86_64
- Working directory: project root (box-selection)
- Command: python manage.py test --verbosity 2
- Exit code: 0

Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

Found 14 test(s).
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, shipping
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying shipping.0001_initial...test_cost_and_volume_tie (shipping.tests.APITests.test_cost_and_volume_tie) ... ok
test_db_constraint (shipping.tests.APITests.test_db_constraint) ... ok
test_dimension_and_volume_rejection (shipping.tests.APITests.test_dimension_and_volume_rejection) ... ok
test_duplicates (shipping.tests.APITests.test_duplicates) ... ok
test_http_errors (shipping.tests.APITests.test_http_errors) ... ok
test_inactive (shipping.tests.APITests.test_inactive) ... ok
test_invalid (shipping.tests.APITests.test_invalid) ... ok
test_page_and_csrf (shipping.tests.APITests.test_page_and_csrf) ... ok
test_unknown (shipping.tests.APITests.test_unknown) ... ok
test_weight_boundary (shipping.tests.APITests.test_weight_boundary) ... ok
test_exact_fit (shipping.tests.PackingTests.test_exact_fit) ... ok
test_randomized_geometry (shipping.tests.PackingTests.test_randomized_geometry) ... ok
test_rotation (shipping.tests.PackingTests.test_rotation) ... ok
test_volume_is_not_enough (shipping.tests.PackingTests.test_volume_is_not_enough) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.058s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

 OK
System check identified no issues (0 silenced).

