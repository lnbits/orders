# Description: Add your page endpoints here.


from fastapi import APIRouter, Depends
from lnbits.core.views.generic import index, index_public
from lnbits.decorators import check_account_exists
from lnbits.helpers import template_renderer

orders_generic_router = APIRouter()


def orders_renderer():
    return template_renderer(["orders/templates"])



# Backend admin page
orders_generic_router.add_api_route("/", methods=["GET"], endpoint=index, dependencies=[Depends(check_account_exists)])


# Frontend shareable page


orders_generic_router.add_api_route("/{orders_id}", methods=["GET"], endpoint=index_public)
