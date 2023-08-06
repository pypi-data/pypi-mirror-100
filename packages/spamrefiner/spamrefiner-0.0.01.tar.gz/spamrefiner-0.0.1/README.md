# SpamRefiner API Python Wrapper
# Basic Usage

```python
import spamrefiner
client = spamrefiner.Client("Your Token Here")
user_id = 777000
flag = client.get_flag(user_id)
reason = client.get_flag_reason(user_id)
if flag:
    print(reason)
else:
    print("Not flagged")
```
