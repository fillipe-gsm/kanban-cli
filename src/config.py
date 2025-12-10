from dynaconf import Dynaconf

# The user can overwrite existing variables with either:
# - creating environment variables starting with `KB_` such as `KB_DB_NAME`; or
# - create a `kb_settings.toml` and add the variables they want
settings = Dynaconf(
    envvar_prefix="KB",
    settings_files=["settings.toml", ".secrets.toml", "kb_settings.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
