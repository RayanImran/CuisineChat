from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import generic_helper
import db_helper

app = FastAPI()

inprogress_orders = {}


@app.get("/")
async def root():
    status = db_helper.get_order_status(40)
    return {"message": status}


@app.post("/")
async def handle_request(request: Request):

    # retrieve the json data from request
    payload = await request.json()
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_context = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_context[0]['name'])
    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'track.order - content: ongoing-tracking':track_order,
        'order.complete - context: ongoing-order':complete_order
    }
    return intent_handler_dict[intent](parameters, session_id)
    # if intent == 'track.order - content: ongoing-tracking':
    #     return track_order(parameters)
    #
    # elif intent == 'order.add - context: ongoing-order':
    #     return add_to_order(parameters)

def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillmentText = "Sorry place a new order again"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillmentText = "Sorry I couldn;t process it"
        else:
            order_total = db_helper.total_price_per_order(order_id)

            fulfillmentText = f"Awesome. We have placed your order. " \
                               f"Here is your order id # {order_id}. " \
                               f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]
        return JSONResponse(content={
            "fulfillmentText": fulfillmentText
        })
def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_iterm(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    return next_order_id




def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillmentText = "Sorry I did not understand specify the quantities"
    else:
        new_food_dict = dict(zip(food_items,quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
    #
    # print("******")
    # print(inprogress_orders)
    order_string = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
    fulfillmentText = f"So far you have: {order_string} do you need anything else?"

    return JSONResponse(content={
            "fulfillmentText": fulfillmentText,
        })

def track_order(parameters: dict):
    order_id = int(parameters['order-id'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillmentText = "The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillmentText = "No order found with order id: {order_id}"


    return JSONResponse(content={
            "fulfillmentText": fulfillmentText,
        })

