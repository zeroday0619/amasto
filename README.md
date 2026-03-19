# amasto

Fully async, type-safe Python client for the [Mastodon API](https://docs.joinmastodon.org/api/).

## Features

- **Async-first** — All I/O uses `async`/`await` via [httpx](https://www.python-httpx.org/)
- **Type-safe** — Typed endpoint descriptors and [Pydantic](https://docs.pydantic.dev/) response models; ships with `py.typed`
- **Version-aware** — Automatic server version detection via NodeInfo; models mark field availability with `since()` / `Unsupported`
- **Minimal surface area** — Small, deliberate public API

## Requirements

- Python **≥ 3.14**

## Installation

```bash
pip install amasto
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add amasto
```

## Quick start

```python
from amasto import Amasto
from amasto.api.v1 import statuses, get_statuses

async def main() -> None:
    client = Amasto("https://mastodon.social", "YOUR_ACCESS_TOKEN")

    # Post a status
    status = await client.fetch(
        statuses.post_statuses,
        body={"status": "Hello from amasto!"},
    )

    # Read a single status by ID
    status = await client.fetch(get_statuses["123456"])
```

## Client

`Amasto` is the main entry point. It wraps an `httpx.AsyncClient` and automatically discovers the server's Mastodon version via the NodeInfo protocol on first use.

```python
from semver import Version

client = Amasto(
    "https://mastodon.social",   # base URL
    "YOUR_ACCESS_TOKEN",         # API key (Bearer token)
    mastodon_version=Version(4, 3, 0),  # optional: skip auto-detection
)
```

### `fetch()`

The `fetch` method has two overloads:

| Form | Return type | Description |
|---|---|---|
| `fetch(endpoint, *, params, body)` | `T` (typed) | Type-safe call using an `Endpoint` descriptor |
| `fetch(method, path, *, params, body)` | `Any` | Raw HTTP call with manual method/path |

## Endpoints

Endpoint descriptors live under `amasto.api` and combine the HTTP method, path, and response type into a single object so that `fetch()` can return fully typed results.

There are three descriptor types:

| Type | Description |
|---|---|
| `Endpoint[T, P, B]` | Fixed-path endpoint |
| `EndpointTemplate[T, P, B]` | Path with a `{param}` placeholder — use `endpoint[key]` to resolve |
| `SubscriptableEndpoint` | Collection + item — flat access for lists, `endpoint[id]` for a single item |

### API v1 (`amasto.api.v1`)

| Module | Endpoints |
|---|---|
| `accounts` | `get_accounts`, `post_accounts`, `accounts[id].*` |
| `announcements` | `get_announcements`, `announcements[id].*` |
| `apps` | `post_apps`, `apps[client_id].*` |
| `blocks` | `get_blocks` |
| `bookmarks` | `get_bookmarks` |
| `conversations` | `get_conversations`, `delete_conversations[id]`, `conversations[id].*` |
| `custom_emojis` | `get_custom_emojis` |
| `directory` | `get_directory` |
| `domain_blocks` | `get_domain_blocks`, `post_domain_blocks`, `delete_domain_blocks` |
| `emails` | `emails.*` |
| `endorsements` | `get_endorsements` |
| `favourites` | `get_favourites` |
| `featured_tags` | `get_featured_tags`, `post_featured_tags`, `delete_featured_tags[id]`, `featured_tags[id].*` |
| `follow_requests` | `get_follow_requests`, `follow_requests[id].*` |
| `followed_tags` | `get_followed_tags` |
| `instance` | `get_instance`, `instance.*` |
| `lists` | `get_lists`, `post_lists`, `put_lists[id]`, `delete_lists[id]`, `lists[id].*` |
| `markers` | `get_markers`, `post_markers` |
| `media` | `get_media[id]`, `put_media[id]`, `delete_media[id]` |
| `mutes` | `get_mutes` |
| `notifications` | `get_notifications`, `notifications[id].*` |
| `polls` | `get_polls[id]`, `polls[id].*` |
| `preferences` | `get_preferences` |
| `profile` | `profile.*` |
| `push` | `push.*` |
| `reports` | `post_reports` |
| `scheduled_statuses` | `get_scheduled_statuses`, `put_scheduled_statuses[id]`, `delete_scheduled_statuses[id]` |
| `search` | `get_search` |
| `statuses` | `get_statuses`, `post_statuses`, `put_statuses[id]`, `delete_statuses[id]`, `statuses[id].*` |
| `suggestions` | `get_suggestions`, `delete_suggestions[id]` |
| `tags` | `get_tags[name]`, `tags[name].*` |
| `timelines` | `timelines.*` |
| `trends` | `trends.*` |

### API v2 (`amasto.api.v2`)

| Module | Endpoints |
|---|---|
| `filters` | `get_filters`, `post_filters`, `put_filters[id]`, `delete_filters[id]`, `filters[id].*` |
| `instance` | `get_instance` |
| `media` | `post_media` |
| `notification_policy` | `notification_policy.*` |
| `notifications` | `get_notifications`, `notifications[id].*` |
| `search` | `get_search` |
| `suggestions` | `get_suggestions` |

### OEmbed (`amasto.api`)

| Endpoint |
|---|
| `get_oembed` |

### OAuth (`amasto.oauth`)

| Endpoint | Description |
|---|---|
| `post_token` | Obtain a token (authorization code / client credentials) |
| `get_authorize` | Authorization URL |
| `get_userinfo` | Authenticated user info |
| `post_revoke` | Revoke a token |

### Health (`amasto.health`)

| Endpoint | Description |
|---|---|
| `get_health` | Server health check |

## Models

Response models live under `amasto.models` and are re-exported from `amasto.models.v1` and `amasto.models.v2`. All models are frozen Pydantic `BaseModel` subclasses.

<details>
<summary>V1 models</summary>

`Account`, `AccountRole`, `AccountSource`, `AccountWarning`, `Announcement`, `AnnouncementAccount`, `AnnouncementStatus`, `Appeal`, `Application`, `AsyncRefresh`, `Context`, `Conversation`, `CredentialAccount`, `CredentialApplication`, `CustomEmoji`, `DomainBlock`, `EncryptedMessage`, `Error`, `ExtendedDescription`, `FamiliarFollowers`, `FeaturedTag`, `Field`, `IdentityProof`, `InstanceStats`, `InstanceUrls`, `List`, `Marker`, `MediaAttachment`, `MutedAccount`, `Notification`, `NotificationRequest`, `Poll`, `PollOption`, `Preferences`, `PreviewCard`, `PreviewCardAuthor`, `PrivacyPolicy`, `Quote`, `QuoteApproval`, `Reaction`, `Relationship`, `RelationshipSeveranceEvent`, `Report`, `Role`, `Rule`, `ScheduledStatus`, `ScheduledStatusParams`, `ScheduledStatusParamsPoll`, `Search`, `ShallowQuote`, `Status`, `StatusEdit`, `StatusEditPoll`, `StatusEditPollOption`, `StatusMention`, `StatusSource`, `StatusTag`, `Suggestion`, `Tag`, `TagHistory`, `TermsOfService`, `Token`, `Translation`, `TranslationAttachment`, `TranslationPoll`, `TranslationPollOption`, `TrendsLink`, `WebPushAlerts`, `WebPushSubscription`

</details>

<details>
<summary>V2 models</summary>

`Filter`, `FilterKeyword`, `FilterResult`, `FilterStatus`, `Instance`, `InstanceConfiguration`, `InstanceConfigurationAccounts`, `InstanceConfigurationMediaAttachments`, `InstanceConfigurationPolls`, `InstanceConfigurationStatuses`, `InstanceConfigurationTimelinesAccess`, `InstanceConfigurationTimelinesFeedAccess`, `InstanceConfigurationTranslation`, `InstanceConfigurationUrls`, `InstanceConfigurationVapid`, `InstanceContact`, `InstanceIcon`, `InstanceRegistrations`, `InstanceThumbnail`, `InstanceThumbnailVersions`, `InstanceUsage`, `InstanceUsageUsers`, `NotificationPolicy`, `NotificationPolicySummary`

</details>

## Version awareness

Model fields annotated with `since("x.y.z")` resolve to `Unsupported` when the connected server is older than the specified version, so your code can safely handle missing data:

```python
from amasto.models import Status
from amasto._version import Unsupported

if not isinstance(status.poll, Unsupported):
    print(status.poll)
```

Endpoints can also declare `requires="x.y.z"` to indicate the minimum server version.

## Dependencies

| Package | Purpose |
|---|---|
| [httpx](https://www.python-httpx.org/) ≥ 0.28.1 | Async HTTP client |
| [pydantic](https://docs.pydantic.dev/) ≥ 2.12.5 | Response validation and models |
| [semver](https://python-semver.readthedocs.io/) ≥ 3.0.4 | Server version parsing |

## License

See [LICENSE](LICENSE) for details.
