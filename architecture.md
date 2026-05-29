# retail ai assistent - architecture 

## overview 

a conversational ai agent that works as personal shopper and customer support assitant for retail clothing store , it uses tool calling to ground every response in real data to prevent hallucination 

## system design 

it follows a loop that goes from reason to act to observe and then repeat 

so 
user input > llm read user message + tool definitions > llm decides which tool to call ( gives structured json) > python  executes the tool against real data > result fed back to llm as context > llm writes final grounded response from that text 

this loop continues until the llm has enough information to answer , it can call multiple tools in one conversation before responding 

## tools 

we have tools like 

search products - that fileters inventory by tags , size, price, sale state and is sorted by best seller score 

get product - it fetches full details of a single product by jd 

get order - retrieves order details using order id 

evaluate return - it applies store policy rules and return eligibility decesion 

## why this structure? 

single agent - it handles both shopping and support , the prompt defines both roles and the tool description guide which tools get called based on user intent , no separate agents needed 

the agent is written from scratch in python , its simple to explain and every decesion in the loop is visible and controllable 

both csvs are loaded into memory resident pandas dataframe when the app starts ,  the stock per size column is parsed from string dict to a real python dict using ast.literal_eval 

in product system tho this would be replaced with a live database connection 

## how hallucination is minimized 

tool description contains explicit instruction for example "never recommend from memory" and "never guess retrun eligbility yourself" 
those are baked into the tool definition , and llm reads before any response 

it only narrates and doesnt decide since all product data comes from search _ products results , it just explains and recommend from waht the tool returns 

the return eligibility is fully deterministic evaluate return is pure python if else logic , llm calls the tools and receives a yes or no decesion with a reason 

there are clean refusal on missing data , the get_order and get_product return none wehn an id is not found and the agent is instructed to refuce clearly rather than fabricate details 


#return policy logic 

the rules are applied in this order 

first clearance - final sale , no return or exchange on it 

second aurelia couture - exchange only , no refund 

nocturne - extended 21 day return window 

sale items - 7 days window , store credit only 

normal items - 14 day window , full refund 

priority order matters here since a clearance item from aurelia couture hits rule 1 before rule 2 


## how tools are selected 

the llm reads tool description on every request and decides which tool fits the user's intent 

so theres shopping query - search_products or get_product for more detail 

return request it goes to evaluate_return - internally feteches order and product 

invalid id - tool returns none agent refused cleanly 

# important 

i chose groq for the use , as anthropic ai was a paid service, but the model works well 

for the model used its 'llama-3.3-70b-versatile' via groq api with temperature = 0 
for deterministic , realiable tool call generation 

