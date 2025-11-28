# Enterprise Edition Setup Guide

This guide explains how to set up and work with the Enterprise Edition of Arka MCP Gateway.

## Architecture Overview

The repository uses a **git submodule** approach:

- **Public Repository** (`arka-mcp-gateway`): Contains community edition with stub files
- **Private Submodule** (`enterprise/`): Contains real enterprise implementations

## For Enterprise Developers (KenisLabs Internal)

### Prerequisites

Before starting, ensure the enterprise repository is pushed to a private remote:

```bash
# If not already done, push enterprise-delta to GitHub
cd /path/to/arka-mcp-gateway-enterprise-delta
git remote add origin git@github.com:kenislabs/arka-mcp-gateway-enterprise.git
git push -u origin main
```

**Important:** Update `.gitmodules` in the community repo with the correct enterprise repository URL.

### Initial Setup

1. **Clone the community repository:**
   ```bash
   git clone https://github.com/kenislabs/arka-mcp-gateway
   cd arka-mcp-gateway
   ```

2. **Initialize the enterprise submodule:**
   ```bash
   git submodule update --init
   ```

   This clones the private enterprise repository into `enterprise/` directory.

   **Note:** You must have access to the private enterprise repository for this to work.

3. **Start the application:**
   ```bash
   cd backend && ./start.sh
   ```

   You should see: `🏢 Edition: ENTERPRISE (Hosted by KenisLabs)`

### Development Workflow

#### Working on Enterprise Features

1. Navigate to the submodule:
   ```bash
   cd enterprise
   ```

2. Make changes to enterprise files:
   - `backend/enterprise/` - Azure SSO implementation
   - `backend/gateway/` - Per-user tool permissions
   - `frontend/src/enterprise/` - Enterprise UI components

3. Commit enterprise changes:
   ```bash
   git add .
   git commit -m "feat: improve azure sso"
   git push
   ```

4. **Important**: Update submodule reference in parent repo:
   ```bash
   cd ..  # Back to arka-mcp-gateway
   git add enterprise
   git commit -m "chore: update enterprise submodule"
   git push
   ```

#### Working on Community Features

1. Stay in the main repository (don't cd into `enterprise/`)

2. Make changes to community files in `backend/` or `frontend/`

3. Commit changes:
   ```bash
   git add backend/somefile.py
   git commit -m "feat: community feature"
   git push
   ```

### How It Works

**Backend Detection** (`backend/config.py`):
- On startup, checks if `enterprise/backend/enterprise/__init__.py` exists
- If yes, adds `enterprise/backend/` to `sys.path`
- Python then imports from enterprise submodule instead of stubs
- Detects `__enterprise__ = True` marker and enables enterprise features

**Frontend Detection** (`frontend/src/enterprise/index.js`):
- Imports from local `enterprise/` module
- When submodule present: imports real implementation
- When submodule absent: imports stubs (returns null components)

### Troubleshooting

**Problem**: Application shows COMMUNITY edition instead of ENTERPRISE

**Solution**: Verify submodule is initialized and populated:
```bash
ls -la enterprise/backend/enterprise/
# Should show __init__.py, auth/, etc.
```

If empty, reinitialize:
```bash
git submodule update --init --recursive
```

---

**Problem**: Changes to enterprise files not reflected

**Solution**: Ensure you're editing files in `enterprise/` directory, not `backend/enterprise/` stubs

---

## For Community Users

Community users will NOT see the enterprise submodule contents:
- Cloning the repository creates an empty `enterprise/` directory
- Application runs with stubs, showing COMMUNITY edition
- All features work except Azure SSO and per-user permissions

---

## Enterprise Features Included

The enterprise submodule provides:

- **Azure AD SSO**: Full OAuth2 integration for Microsoft/Office 365 login
- **Per-User Tool Permissions**: Granular control over which users can access which tools

All other features (GitHub OAuth, user management, tool permissions) are available in the community edition.

---

## Architecture Benefits

✅ **No file copying**: Changes in submodule are instantly reflected
✅ **Clear commit boundaries**: Enterprise commits go to enterprise repo, community to community repo
✅ **HMR works**: Hot module reload detects changes in both repos
✅ **Simple for community**: They never see enterprise code
✅ **Single codebase**: One repository to maintain, submodule for extensions

---

## Additional Resources

- [Monorepo Consolidation Summary](localdocs/MONOREPO_CONSOLIDATION_SUMMARY.md) - Implementation details
- [Backend README](backend/README.md) - Backend architecture
- [Frontend README](frontend/README.md) - Frontend architecture

For enterprise support, contact: enterprise@kenislabs.com
