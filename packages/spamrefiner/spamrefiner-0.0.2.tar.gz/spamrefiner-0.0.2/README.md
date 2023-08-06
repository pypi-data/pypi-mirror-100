# SpamRefiner API Python Wrapper
# Basic Usage

```python
import spamrefiner
client = spamrefiner.Client("Your Token Here")
user_id = 777000
flag = client.get_flag(user_id)
try:
    print(f"This user is flagged with reason: {flag.reason}")
except:
    print(f"{flag}")
```
