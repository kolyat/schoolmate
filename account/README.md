# Account


### Authentication API

This application uses standard Django's API for authentication and user
management.

| Endpoint | Description |
| -------- | ----------- |
| `/profile/login/` | Log in |
| `/profile/logout/` | Log out |
| `/profile/password_reset/` | Password reset request |
| `/profile/password_reset/email/` | 'E-mail has been sent' message after password reset request |
| `/profile/password_reset/<uidb64>/<token>/` | New password setup interface |
| `/profile/password_reset/complete/` | Message after successful password setup |
| `/profile/password_change/` | Password change interface |
| `/profile/password_change/done/` | Endpoint for redirection after successful password change |

See [official Django documentation](https://docs.djangoproject.com/en/2.0/topics/auth/)
for further details.
