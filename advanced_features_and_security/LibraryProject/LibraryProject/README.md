# Django Permissions and Groups System

## Overview
This system implements role-based access control using Django's built-in permissions and groups.

## Groups and Permissions

### Groups
1. **Viewers** - Can view articles
2. **Editors** - Can view, create, and edit articles
3. **Admins** - Full permissions (view, create, edit, delete)

### Permissions
- `can_view` - View article listings and details
- `can_create` - Create new articles
- `can_edit` - Edit existing articles
- `can_delete` - Delete articles

## Setup
1. Run migrations:
   ```bash
   python manage.py migrate