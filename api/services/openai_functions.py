from pydantic import BaseModel, Field

    
class FunctionSchema(BaseModel):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        schema = cls.schema()
        obj = {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": {
                "type": "object",
                "properties": schema["properties"]
            }
        }
        if "required" in schema:
            obj["parameters"]["required"] = schema["required"]
            
        if "examples" in schema:
            obj["examples"] = schema["examples"]
            
        if "default" in schema:
            obj["default"] = schema["default"]

        cls.json_schema = obj
        
    
