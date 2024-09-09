import inspect

CODING_TEMPLATE = inspect.cleandoc(
    """
You're a software engineer at a company that has a large codebase. You're tasked with adding a new feature to the codebase. 
The codebase is written in {language} using the {framework} framework. The feature is to {feature}.
Write the code that implements this feature.

"""
)
