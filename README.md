# O,Data STAR
<p align="center">
  <img src="https://i.ibb.co/12Xz2wB/Group-1.png" />
</p>
<br><br>
O,Data STAR is a web app that allows the user to put in complex documents as input and ask queries or suggest recommendations based on the data in those documents.
<br><br>
To check out the user interface, visit: https://odatastar.co/
<br>
To check the whole project, visit: https://www.spaceappschallenge.org/2023/find-a-team/the-procrastinators/?tab=project

## Installation
Run the following command on your terminal to install all the required packages,
```
pip install langchain openai chromadb tiktoken flask werkzeug "unstructured[all-docs]"
```

Create or edit the "*envs.py*" file and enter your [OpenAI api key](https://platform.openai.com/account/api-keys),
```python
APIKEY="<Your API key here>"
```

### Common Errors
If you are getiing an error with the package "**numexpr**" on a windows machine, please install the MS Visual C++ runtime ([VC_redist.x64.exe](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)).
