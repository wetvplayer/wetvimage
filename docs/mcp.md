# ⚡ MyTVPro MCP Server Automation Documentation

Complete guide for automating your IPTV panel via the MyTVPro MCP JSON-RPC interface, including category management, bouquet structures, channel import, CDN logo updating, and Line/Package permission assignments.

---

## 📌 Table of Contents
1. [Overview & MCP Connection](#overview--mcp-connection)
2. [Unified MCP Uploader (`mcp/upload_to_mcp.py`)](#unified-mcp-uploader-mcpupload_to_mcppy)
   - [Basic Usage](#basic-usage)
   - [Custom Category & Bouquet Selection](#custom-category--bouquet-selection)
   - [Line & User Assignments](#line--user-assignments)
   - [Full CLI Options](#full-cli-options)
3. [Category & Bouquet Consolidation (`mcp/merge_all_sports.py`)](#category--bouquet-consolidation-mcpmerge_all_sportspy)
4. [Inspecting Server Status (`mcp/list_categories.py`, `mcp/check_line_bouquets.py`)](#inspecting-server-status)
5. [Restoring All Bouquets to Lines (`mcp/assign_all_bouquets_to_line.py`)](#restoring-all-bouquets-to-lines)
6. [Core Architecture: Line vs User](#core-architecture-line-vs-user)

---

## 1. Overview & MCP Connection

The MyTVPro MCP server provides programmatic JSON-RPC control over:
- **`category-manager`**: Create, read, update, list, and delete Live, Movie, and Series categories.
- **`bouquet-manager`**: Manage bouquets and assign channels, movies, series, and lines.
- **`channel-manager`**: Manage live channel streams, logos, and category bindings.
- **`line-manager`**: Manage IPTV client subscription accounts (`username: 123`) and their assigned bouquet lists.
- **`package-manager`**: Manage VIP subscription packages and link bouquet bundles.
- **`m3u-importer`**: Bulk import and update streams directly from M3U playlist text.

---

## 2. Unified MCP Uploader (`mcp/upload_to_mcp.py`)

The `upload_to_mcp.py` tool handles the entire end-to-end sync workflow:
1. Reads your CDN-linked playlist (e.g. `playlists/sports_github.m3u`).
2. Creates or locates the target **Category** and **Bouquet**.
3. Imports and updates matching stream URLs with your **GitHub CDN logo images**.
4. Assigns all channels to the target Bouquet.
5. **Safely retains all existing bouquets** on the Line and packages while attaching the new bouquet.

### Basic Usage:
```powershell
# Default: Uploads CDN playlist, sets category & bouquet to 'All Sports', assigns to Line '123' and all VIP packages
py mcp/upload_to_mcp.py
```

### Custom Category, Bouquet & Line:
```powershell
# Specify custom category, custom bouquet, and target line username:
py mcp/upload_to_mcp.py --m3u playlists/sports_github.m3u --category "Sports HD" --bouquet "Sports VIP" --line "123"
```

### Assign to All Active Users / Lines:
```powershell
py mcp/upload_to_mcp.py --line all
```

### Full CLI Options:
| Flag | Default | Description |
| :--- | :--- | :--- |
| `--m3u` | `playlists/sports_github.m3u` | Path to M3U playlist file |
| `--category` | `All Sports` | Target live category name |
| `--bouquet` | `All Sports` | Target bouquet name |
| `--line` / `--user` | `123` | Line username or ID (or `all`) |
| `--no-packages` | `False` | Skip linking bouquet to VIP packages |

---

## 3. Category & Bouquet Consolidation (`mcp/merge_all_sports.py`)

If your playlist has fragmented sports categories (`SPORTS`, `Russian Sports`, `ALWAN SPORTS`, `MIX SPORTS`) and you want to clean up your panel into a single **`All Sports`** category and bouquet:

```powershell
py mcp/merge_all_sports.py
```
- Moves all sports channels into Category ID `105` (`All Sports`).
- Deletes redundant sports categories and bouquets.
- Updates Line 123 and VIP packages with the unified `All Sports` bouquet (ID: `69`).
- Updates `playlists/sports.m3u` locally with `group-title="All Sports"`.

---

## 4. Inspecting Server Status

### List All Categories & Live Counts:
```powershell
py mcp/list_categories.py
```
Outputs total channels/movies/series count for every category across Live TV, Movies, and Series.

### Check Assigned Bouquets on Line 123:
```powershell
py mcp/check_line_bouquets.py
```
Displays all bouquets currently active on Line 123 and lists all 58 available bouquets on the server.

---

## 5. Restoring All Bouquets to Lines

To assign **ALL 58 bouquets** (Movies, Series, Live TV, Kurdish Channels, Arabic, Islamic, Kids, All Sports) to Line 123 and all VIP packages:

```powershell
py mcp/assign_all_bouquets_to_line.py
```

---

## 6. Removing & Deleting Items (`mcp/remove_from_mcp.py`)

Tools to safely delete categories, bouquets, or entire playlists from the server:

### Option A: Delete a Category & Its Channels
```powershell
# Delete category by name or ID:
py mcp/remove_from_mcp.py --category "Old Category"
py mcp/remove_from_mcp.py --category 111
```

### Option B: Delete a Bouquet
```powershell
# Deletes the bouquet and automatically detaches it from all Lines and Packages:
py mcp/remove_from_mcp.py --bouquet "Old Bouquet"
```

### Option C: Delete All Channels from a Playlist
```powershell
# Deletes all server channels that match the stream URLs in a playlist:
py mcp/remove_from_mcp.py --playlist "playlists/old_playlist.m3u"
```

### Option D: Clean Up Empty Categories (0 Channels)
```powershell
py mcp/remove_from_mcp.py --clean-empty
```

---

## 7. Core Architecture: Line vs User

| Concept | Purpose | Where Managed | Examples |
| :--- | :--- | :--- | :--- |
| **Line** | Streaming subscription account for IPTV players (TiviMate, Smarters) | `line-manager` | `username: 123`, `password: 123` |
| **User** | Admin / Reseller portal account for the web control dashboard | `user-manager` | Admin login email & password |

> [!NOTE]
> Channels and bouquets are assigned to **Lines** so the IPTV player application receives the channel playlist. Our tooling supports `--line` and `--user` interchangeably.

