# src/schemas/context/updater.py
from .typed_schema import ContextUpdate, ConversationContext

def update_context(
    context: ConversationContext,
    extracted: ContextUpdate
) -> ConversationContext:
    """
    Merge a newly extracted ContextUpdate into the stored ConversationContext.
    """

    if extracted.domain:
        context.active_domain = extracted.domain

    if extracted.intent:
        context.last_intent = extracted.intent

    entity_data = extracted.entities.model_dump(exclude_none=True)
    if entity_data:
        context.last_entities.update(entity_data)

    pref_data = extracted.preferences.model_dump(exclude_none=True)
    if pref_data:
        context.preferences.update(pref_data)

    inferred_data = extracted.inferred_defaults.model_dump(exclude_none=True)
    if inferred_data:
        context.memory.update(inferred_data)

    if extracted.aggregation and extracted.aggregation != "none":
        context.memory["aggregation"] = extracted.aggregation

    context.unresolved_slots = extracted.missing_slots

    return context