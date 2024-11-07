## 🚀 Pull Request Template

### Description

<!-- Please provide a summary of what this PR is about. What problem does it solve? What changes have been made? -->

---

### Checklist

- [ ] **Code Formatting**
  - [ ] Code adheres to the project's style guide ('black .' is run from project root)
  - [ ] No unnecessary print statements or debugging code
  - [ ] Proper docstrings and comments where necessary

- [ ] **Tests**
  - [ ] Necessary unit tests have been added or modified
  - [ ] Tests pass locally (`pytest` or other test framework)
  - [ ] Coverage is adequate (aim for > 80%)

- [ ] **FastAPI/REST API Checks**
  - [ ] Correct usage of FastAPI endpoints (e.g., `GET`, `POST`, `PUT`, `DELETE`)
  - [ ] Proper validation of request/response models
  - [ ] Authentication and authorization (if applicable) is properly implemented
  - [ ] Appropriate HTTP status codes are used in responses (e.g., `200 OK`, `201 Created`, `400 Bad Request`, etc.)

- [ ] **Documentation**
  - [ ] API documentation is up-to-date (use FastAPI's auto-generated docs or custom documentation)
  - [ ] API endpoints are properly documented with descriptions and request/response models

- [ ] **Security**
  - [ ] Input validation/sanitization is applied to prevent SQL injection or other vulnerabilities
  - [ ] Sensitive data handling (e.g., passwords, API keys) is done securely

- [ ] **Deployment & Environment** (if applicable)
  - [ ] Environment variables and configuration settings are properly handled
  - [ ] Docker support (if applicable): `Dockerfile` and `docker-compose.yml` are up to date
  - [ ] `Makefile` or other deployment scripts (if applicable) have been updated

---

### Related Issues

<!-- List any related issues (e.g., `Fixes #123`, `Closes #456`, etc.) -->

---

### Additional Notes (Optional)

<!-- Add any other information or context that reviewers should be aware of. -->

---

### Screenshots (Optional)

<!-- If applicable, include screenshots or relevant output to help reviewers understand the changes. -->
