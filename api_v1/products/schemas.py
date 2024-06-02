from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(max_length=50)
    price: int = Field(ge=1)
    description: str = Field(min_length=5)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    price: int | None = None
    description: str | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
