Tested metis agent permissions: edit, bash, webfetch.

- Actions performed:
  - Created test file tests/metis_edit_permission_test.txt with content "METIS EDIT PERMISSION TEST: OK" to verify edit permission.
  - Verified edit by checking file existence and content via bash command. Result: FILE_EXISTS, CONTENT_OK.
  - Used webfetch to fetch https://example.com to verify webfetch permission. Result: retrieved content (non-empty).
  - Cleaned up test file from filesystem. Result: file removed.

- Results:
  - edit permission: PASS
  - bash permission: PASS
  - webfetch permission: PASS

- Notes:
  - lsp diagnostics could not be run on .txt; no LSP server configured for .txt extension.
  - All test artifacts were cleaned up.
