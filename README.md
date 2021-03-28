# VKSlaves
Asynchronous api wrapper for the game from vk.com called "slaves"

# Example of usage
```python
import asyncio
from vkslaves import Slaves

slaves_api = Slaves(app_auth="vk_access_token_settings=friends,status&vk_app_id=7794757...")


async def main():
    await slaves_api.start()  # update .me and .slaves
    print(slaves_api.me.balance) # get your balance
    user = slaves_api.user(id=1) # get info about vk.com/id1
    print(user.master_id) # get id of user's master

asyncio.run(main())
```

### I'm too lazy to write documentation, just look at the names of the functions and docstrings