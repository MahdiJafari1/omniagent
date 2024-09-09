import os
from functools import cached_property
from typing import Type, Union, List, Optional

import backoff
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableWithFallbacks
from openai import APIConnectionError, APIError, APITimeoutError, RateLimitError

from app.core.logging import app_logger

logger = app_logger.get_logger(__name__)


class Executor:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model_name = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    @cached_property
    def model(self) -> RunnableWithFallbacks:
        main_model = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.0,
            max_tokens=1000,
            api_key=self.api_key,
        )
        backup_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.0,
            max_tokens=1000,
            api_key=self.api_key,
        )
        return main_model.with_fallbacks([backup_model])

    @staticmethod
    def get_parser(output_object: Type[BaseModel] | None):
        return (
            JsonOutputParser(pydantic_object=output_object)
            if output_object
            else StrOutputParser()
        )

    @backoff.on_exception(
        backoff.expo,
        exception=(RateLimitError, APIError, APIConnectionError, APITimeoutError),
        max_tries=5,
        on_backoff=lambda details: logger.warning(
            f"Executor.execute: Retry attempt {details['tries']} after {details['wait']} seconds due to {details['exception']}"
        ),
    )
    def execute(
        self,
        prompt: Union[PromptTemplate, List[PromptTemplate]],
        args: dict,
        output_object: Type[BaseModel] | None = None,
        description: Optional[str] = "Executing prompt",
    ):
        try:
            parser = self.get_parser(output_object)
            chain = prompt | self.model | parser if args else self.model | parser

            logger.info(f"{description} using model {self.model_name}")
            result = chain.invoke(args if args else prompt)
            logger.success(f"Executor.execute: {result}")

            return result
        except Exception as e:
            logger.error(f"Exception in Executor.execute: {e}")
            raise

    @backoff.on_exception(
        backoff.expo,
        exception=(RateLimitError, APIError, APIConnectionError, APITimeoutError),
        max_tries=5,
        on_backoff=lambda details: logger.warning(
            f"Executor.batch_execute: Retry attempt {details['tries']} after {details['wait']} seconds due to {details['exception']}"
        ),
    )
    def batch_execute(
        self,
        prompts: List[PromptTemplate],
        args: dict,
        output_object: Type[BaseModel] | None = None,
        description: Optional[str] = "Executing batch prompts",
    ) -> dict:
        try:
            parser = self.get_parser(output_object)
            chain = prompts | self.model | parser if args else self.model | parser

            logger.info(f"{description} using model {self.model_name}")
            results = chain.batch(args if args else prompts)
            logger.success(f"Executor.batch_execute: {results}")

            return results
        except Exception as e:
            logger.error(f"Exception in Executor.batch_execute: {e}")
            raise
