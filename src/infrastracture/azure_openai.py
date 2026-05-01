from ..utils.logger import setup_logger
from ..core.config import get_settings
from openai import AsyncAzureOpenAI
# from ..models.orchestrator import ConversationContext
from typing import Dict, Any, List
import json
from ..schemas.context.canonical_schema import CANONICAL_CONTEXT_UPDATE_SCHEMA
from ..schemas.context.typed_schema import ContextUpdate, ConversationContext
from pydantic import ValidationError
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionMessageParam, ChatCompletionSystemMessageParam
from ..schemas.tools.json_schema import FLIGHT_TOOLS
from src.schemas.tools.typed_schema import TOOL_ARG_MODELS
from ..schemas.context.json_schema import CONTEXT_UPDATE_JSON_SCHEMA
from openai.types.shared_params.response_format_json_schema import ResponseFormatJSONSchema
from ..schemas.context.updater import update_context
from semantic_kernel.functions import KernelArguments

logger = setup_logger(__name__)

class AzureOpenAIService:
    def __init__(self, kernel):
        self.kernel = kernel
        settings = get_settings()
        # openai.api_type = "azure"
        # openai.api_base = settings.azure_openai_endpoint
        # openai.api_version = settings.azure_openai_api_version
        # openai.api_key = settings.azure_openai_api_key
        self.client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )
        self.deployment_name = settings.azure_openai_deployment_name

#     async def extract_message_data_llm(
#         self,
#         message: str,
#         context: ConversationContext
#     ) -> Dict[str, Any]:
#         """
#         Extract a structured context update from the user message.
#         Returns a validated dict matching ContextUpdate.
#         """
#
#         prompt = f"""
# You are extracting structured flight assistant context updates.
#
# Return ONLY valid JSON.
# Do not include markdown.
# Do not include explanation text.
#
# The JSON must follow this canonical schema:
# {json.dumps(CANONICAL_CONTEXT_UPDATE_SCHEMA, indent=2)}
#
# Known conversation context:
# {json.dumps(context.model_dump(), indent=2)}
#
# User message:
# {message}
# """
#
#         response = await self._get_completion(prompt)
#
#         try:
#             raw_data = json.loads(response)
#         except json.JSONDecodeError:
#             logger.error("Invalid JSON from LLM: %s", response)
#             return ContextUpdate().model_dump()
#
#         try:
#             validated = ContextUpdate.model_validate(raw_data)
#             return validated.model_dump(exclude_none=True)
#         except ValidationError as e:
#             logger.error("ContextUpdate validation failed: %s", e)
#             logger.error("Raw LLM JSON: %s", raw_data)
#             return ContextUpdate().model_dump()
#
#     async def _get_completion(self, prompt: str) -> str:
#         try:
#             messages: list[ChatCompletionUserMessageParam] = [
#                 ChatCompletionUserMessageParam(
#                     role="user",
#                     content=prompt
#                 )
#             ]
#
#             response = await self.client.chat.completions.create(
#                 model=self.deployment_name,
#                 messages=messages,
#                 temperature=0.2,
#                 max_tokens=800,
#             )
#             return response.choices[0].message.content or ""
#
#         except Exception:
#             logger.exception("Error getting completion")
#             raise

    #     async def extract_message_data_llm(
    #         self,
    #         message: str,
    #         context: ConversationContext
    #     ) -> Dict[str, Any]:
    #
    #         prompt = f"""
    # Extract structured travel data from the user message.
    #
    # Return ONLY valid JSON in this format:
    # {{
    #   "intent": string or null,
    #   "entities": {{
    #     "location": string,
    #     "activity_type": string,
    #     "date": string,
    #     "participants": int
    #   }},
    #   "preferences": {{
    #     "budget": string,
    #     "family_friendly": boolean
    #   }},
    #   "memory": {{
    #     "traveling_with_children": boolean
    #   }}
    # }}
    #
    # Known context:
    # {json.dumps(context.model_dump(), indent=2)}
    #
    # User message:
    # {message}
    # """
    #
    #         response = await self._get_completion(prompt)
    #
    #         try:
    #             return json.loads(response)
    #         except json.JSONDecodeError:
    #             logger.error(f"Invalid JSON from LLM: {response}")
    #             return {}
    # async def _get_completion(self, prompt: str) -> str:
    #     try:
    #         response = await self.client.chat.completions.create(
    #             model=self.deployment_name,
    #             messages=[{"role": "user", "content": prompt}],
    #             temperature=0.7,
    #             max_tokens=800,
    #         )
    #         return response.choices[0].message.content or ""
    #     except Exception as e:
    #         logger.exception("Error getting completion")
    #         raise

    async def process_message(
        self,
        message: str,
        context: ConversationContext
    ) -> Dict[str, Any]:
        """
        One full loop:
        1. Ask model to extract context and choose a tool if needed
        2. Validate extracted context
        3. Execute tool if requested
        4. Send tool result back to model for final answer
        """

#         messages: List[ChatCompletionMessageParam] = [
#             {
#                 "role": "system",
#                 "content": f"""
# You are a flight assistant.
#
# First, understand the user's message using this canonical schema:
# {json.dumps(CANONICAL_CONTEXT_UPDATE_SCHEMA, indent=2)}
#
# Rules:
# - Decide the user's primary intent.
# - Extract entities, preferences, defaults, and missing slots.
# - If external flight data is needed, call the most appropriate tool.
# - If no tool is needed, answer directly.
# - Prefer tool calls for:
#   - get_flight_details
#   - search_flights
#   - count_flights
#   - list_flights
# """
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Known conversation context:
# {json.dumps(context.model_dump(), indent=2)}
#
# User message:
# {message}
# """
#             }
#         ]

        system_prompt = f"""
        You are a flight assistant.

        First, understand the user's message using this canonical schema:
        {json.dumps(CANONICAL_CONTEXT_UPDATE_SCHEMA, indent=2)}

        Rules:
        - Decide the user's primary intent.
        - Extract entities, preferences, defaults, and missing slots.
        - If external flight data is needed, call the most appropriate tool.
        - If no tool is needed, answer directly.
        - Prefer tool calls for:
          - get_flight_details
          - search_flights
          - count_flights
          - list_flights
        """

        user_prompt = f"""
        Known conversation context:
        {json.dumps(context.model_dump(), indent=2)}

        User message:
        {message}
        """

        system_message: ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": system_prompt,
        }

        user_message: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": user_prompt,
        }

        messages: list[ChatCompletionMessageParam] = [
            system_message,
            user_message,
        ]

        response = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            tools=FLIGHT_TOOLS,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=800,
        )

        assistant_message = response.choices[0].message

        # Case 1: model requested a tool
        if assistant_message.tool_calls:
            # return await self._handle_tool_call(messages, assistant_message)
            return await self._handle_tool_call(message, context, messages, assistant_message)

        # Case 2: model answered directly in content
        content = assistant_message.content or ""

        extracted = await self.extract_message_data_llm(message, context)
        updated_context = update_context(context, extracted) # we use the extract_message_data_llm() result which is in ContextUpdate format to run update_context which also uses ContextUpdate format

        return {
            "decision_type": "final",
            "context_update": updated_context, # use this to update context at orchestrator.py
            "response": content, # use this to append message at orchestrator.py and also return this response to frontend
        }

    async def extract_message_data_llm(
        self,
        message: str,
        context: ConversationContext
    ) -> ContextUpdate:
    # ) -> Dict[str, Any]:

#         prompt = f"""
# You are extracting structured flight assistant context updates.
#
# Return ONLY valid JSON.
# Do not include markdown.
# Do not include explanation text.
#
# The JSON must follow this canonical schema:
# {json.dumps(CANONICAL_CONTEXT_UPDATE_SCHEMA, indent=2)}
#
# Known conversation context:
# {json.dumps(context.model_dump(), indent=2)}
#
# User message:
# {message}
# """
        prompt = f"""
        You extract structured context updates for a flight assistant.

        Interpret the user message using the provided schema and the known conversation context.

        Rules:
        - Choose the single best intent.
        - Extract only information that is explicitly stated or strongly implied.
        - Leave unknown fields as null.
        - Use empty arrays where appropriate.
        - Do not invent values.
        - Use known conversation context only when it helps resolve omitted but clearly intended details.
        - Populate missing_slots with any important information still needed to fulfill the request.
        - Set requires_tool to true when external flight data is needed to answer the request.
        - Set confidence as a float between 0 and 1.

        Canonical schema reference:
        {json.dumps(CANONICAL_CONTEXT_UPDATE_SCHEMA, indent=2)}

        Known conversation context:
        {json.dumps(context.model_dump(), indent=2)}

        User message:
        {message}
        """

        response = await self._get_text_completion(prompt)

        try:
            raw_data = json.loads(response)
        except json.JSONDecodeError:
            logger.error("Invalid JSON from LLM: %s", response)
            return ContextUpdate()

        try:
            validated = ContextUpdate.model_validate(raw_data) # Since _get_text_completion() returns CONTEXT_UPDATE_JSON_SCHEMA format, we use this validation to convert it back to ContextUpdate format.
            # return validated.model_dump(exclude_none=True)
            return validated
        except ValidationError as e:
            logger.error("ContextUpdate validation failed: %s", e)
            logger.error("Raw LLM JSON: %s", raw_data)
            return ContextUpdate()

    # async def _get_text_completion(self, prompt: str) -> str:
    #     try:
    #         messages: list[ChatCompletionUserMessageParam] = [
    #             ChatCompletionUserMessageParam(
    #                 role="user",
    #                 content=prompt
    #             )
    #         ]
    #
    #         response = await self.client.chat.completions.create(
    #             model=self.deployment_name,
    #             messages=messages,
    #             temperature=0.2,
    #             max_tokens=800,
    #         )
    #         return response.choices[0].message.content or ""
    #     except Exception:
    #         logger.exception("Error getting completion")
    #         raise

    async def _get_text_completion(self, prompt: str) -> str:
        try:
            messages: list[ChatCompletionUserMessageParam] = [
                ChatCompletionUserMessageParam(
                    role="user",
                    content=prompt
                )
            ]

            response_format: ResponseFormatJSONSchema = {
                "type": "json_schema",
                "json_schema": {
                    "name": "context_update",
                    "strict": True,
                    "schema": CONTEXT_UPDATE_JSON_SCHEMA,
                },
            }

            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.0,  # 🔴 important for structured output
                max_tokens=800,
                response_format=response_format,
                # response_format={
                #     "type": "json_schema",
                #     "json_schema": {
                #         "name": "context_update",
                #         "strict": True,
                #         "schema": CONTEXT_UPDATE_JSON_SCHEMA
                #     }
                # }
            )

            return response.choices[0].message.content or ""

        except Exception:
            logger.exception("Error getting completion")
            raise

    async def _handle_tool_call(
        self,
        message: str, # can remove this but it's not being used
        context: ConversationContext,
        messages: List[ChatCompletionMessageParam],
        assistant_message
    ) -> Dict[str, Any]:
        tool_call = assistant_message.tool_calls[0]
        tool_name = tool_call.function.name
        raw_args = tool_call.function.arguments

        try:
            tool_args = json.loads(raw_args)
        except json.JSONDecodeError:
            logger.error("Invalid tool JSON args: %s", raw_args)
            return {
                "decision_type": "error",
                "response": "The model returned invalid tool arguments."
            }
        # fall back to raw tool_args due to kernel_args = KernelArguments(**clean_tool_args)
        clean_tool_args = tool_args

        model_cls = TOOL_ARG_MODELS.get(tool_name)

        if model_cls:
            try:
                validated_args = model_cls.model_validate(tool_args)
                # So we replaced the raw tool_args with the validated_args
                clean_tool_args = validated_args.model_dump(exclude_none=True)
            except ValidationError:
                logger.exception("Tool args validation failed")
                return {
                    "decision_type": "error",
                    "response": f"Invalid arguments for {tool_name}"
                }

        # # local function call
        # if tool_name == "get_flight_details":
        #     tool_result = await self.get_flight_details(**tool_args)
        # elif tool_name == "search_flights":
        #     tool_result = await self.search_flights(**tool_args)
        # elif tool_name == "count_flights":
        #     tool_result = await self.count_flights(**tool_args)
        # elif tool_name == "list_flights":
        #     tool_result = await self.list_flights(**tool_args)
        # else:
        #     return {
        #         "decision_type": "error",
        #         "response": f"Unknown tool: {tool_name}"
        #     }

        # # Method 1: direct call
        # tool_map = {
        #     "get_flight_details": self.flight_skill.get_flight_details,
        #     "search_flights": self.flight_skill.search_flights,
        #     "count_flights": self.flight_skill.count_flights,
        #     "list_flights": self.flight_skill.list_flights,
        # }
        #
        # tool_fn = tool_map.get(tool_name)
        # if not tool_fn:
        #     return {
        #         "decision_type": "error",
        #         "response": f"Unknown tool: {tool_name}"
        #     }
        #
        # tool_result = await tool_fn(**tool_args)

        # Method 2: SK call
        try:
            kernel_args = KernelArguments(**clean_tool_args) # without clean_tool_args = tool_args this will have error

            tool_result = await self.kernel.invoke(
                plugin_name="flight_skill",
                function_name=tool_name,
                arguments=kernel_args
            )

            # SK may return a FunctionResult-like object, not plain dict/string
            if hasattr(tool_result, "value"):
                serializable_result = tool_result.value
            else:
                serializable_result = str(tool_result)

        except Exception:
            logger.exception("Kernel tool invocation failed for %s", tool_name)
            return {
                "decision_type": "error",
                "response": f"Failed to execute tool: {tool_name}",
            }

        # followup_messages: List[ChatCompletionMessageParam] = [
        #     *messages,
        #     {
        #         "role": "assistant",
        #         "tool_calls": [
        #             {
        #                 "id": tool_call.id,
        #                 "type": "function",
        #                 "function": {
        #                     "name": tool_name,
        #                     "arguments": raw_args,
        #                 }
        #             }
        #         ]
        #     },
        #     {
        #         "role": "tool",
        #         "tool_call_id": tool_call.id,
        #         "content": json.dumps(serializable_result),
        #     }
        # ]
        '''send tool result back to model'''
        followup_messages: List[ChatCompletionMessageParam] = [
            *messages,
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(clean_tool_args),
                        }
                    }
                ]
            },
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(serializable_result),
            }
        ]


        # this is to produce final natural-language answer
        final_response = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=followup_messages,
            temperature=0.2,
            max_tokens=800,
        )

        final_text = final_response.choices[0].message.content or ""

        # return {
        #     "decision_type": "tool_call",
        #     "tool_name": tool_name,
        #     "tool_args": tool_args,
        #     "tool_result": tool_result,
        #     "response": final_text,
        # }

        # enrich with tool info
        updated_context = context.model_copy(deep=True)
        # extracted = await self.extract_message_data_llm(message, context)
        # updated_context = update_context(context, extracted)
        updated_context.memory.setdefault("tool_state", {})
        updated_context.memory["tool_state"]["last_tool"] = {
            "name": tool_name,
            "args": clean_tool_args,  # <- converted 15-min args are here
            "result": serializable_result,
        }
        # updated_context.memory["last_tool_name"] = tool_name
        # updated_context.memory["last_tool_args"] = tool_args

        return {
            "decision_type": "tool_call",
            "tool_name": tool_name,
            "tool_args": clean_tool_args,
            "tool_result": serializable_result,
            "context_update": updated_context,
            "response": final_text,
        }

    # ----- stub tool functions -----
    # async def get_flight_details(
    #     self,
    #     flight_number: str | None = None,
    #     callsign: str | None = None,
    #     icao24: str | None = None,
    #     date: str | None = None,
    #     airport: str | None = None,
    # ) -> Dict[str, Any]:
    #     return {
    #         "flight_number": flight_number,
    #         "callsign": callsign,
    #         "icao24": icao24,
    #         "date": date,
    #         "airport": airport,
    #         "status": "scheduled"
    #     }
    #
    # async def search_flights(
    #     self,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     origin_city: str | None = None,
    #     destination_city: str | None = None,
    #     date: str | None = None,
    #     time_from: str | None = None,
    #     time_to: str | None = None,
    #     max_results: int | None = 10,
    # ) -> Dict[str, Any]:
    #     return {
    #         "matches": [],
    #         "filters": {
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "airport": airport,
    #             "direction": direction,
    #             "origin_city": origin_city,
    #             "destination_city": destination_city,
    #             "date": date,
    #             "time_from": time_from,
    #             "time_to": time_to,
    #             "max_results": max_results,
    #         }
    #     }
    #
    # async def count_flights(
    #     self,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     date: str | None = None,
    # ) -> Dict[str, Any]:
    #     return {
    #         "count": 0,
    #         "filters": {
    #             "airport": airport,
    #             "direction": direction,
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "date": date,
    #         }
    #     }
    #
    # async def list_flights(
    #     self,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     date: str | None = None,
    #     time_from: str | None = None,
    #     time_to: str | None = None,
    #     max_results: int | None = 10,
    # ) -> Dict[str, Any]:
    #     return {
    #         "flights": [],
    #         "filters": {
    #             "airport": airport,
    #             "direction": direction,
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "date": date,
    #             "time_from": time_from,
    #             "time_to": time_to,
    #             "max_results": max_results,
    #         }
    #     }