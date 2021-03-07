# https://marmelab.com/react-admin/Fields.html
# Fields mapping from tortoise to react
tortoise_fields_mapping = {
    "CharField": "ReactAdmin.TextField",
    "BooleanField": "ReactAdmin.BooleanField",
    "DateField": "ReactAdmin.DateField",
    "DatetimeField": "ReactAdmin.DateField",
    "UUIDField": "ReactAdmin.TextField",
    "EmailField": "ReactAdmin.EmailField",
    "UrlField": "ReactAdmin.UrlField",
    "RichTextField": "ReactAdmin.RichTextField",
    "ChipField": "ReactAdmin.ChipField",
    "IntField": "ReactAdmin.NumberField",
    "BigIntField": "ReactAdmin.NumberField",
    "SmallIntField": "ReactAdmin.NumberField",
    "TextField": "ReactAdmin.TextField",
    "DecimalField": "ReactAdmin.NumberField",
}


# https://marmelab.com/react-admin/Inputs.html
# Inputs mapping from tortoise to react
tortoise_inputs_mapping = {
    "CharField": "ReactAdmin.TextInput",
    "BooleanField": "ReactAdmin.BooleanInput",
    "DateField": "ReactAdmin.DateInput",
    "DatetimeField": "ReactAdmin.DateTimeInput",
    "UUIDField": "ReactAdmin.TextInput",
    "EmailField": "ReactAdmin.TextInput",
    "UrlField": "ReactAdmin.TextInput",
    "RichTextField": "ReactAdmin.RichTextInput",
    "ChipField": "ReactAdmin.TextInput",
    "IntField": "ReactAdmin.NumberInput",
    "BigIntField": "ReactAdmin.NumberInput",
    "SmallIntField": "ReactAdmin.NumberInput",
    "TextField": "ReactAdmin.TextInput",
    "DecimalField": "ReactAdmin.NumberInput",
}
