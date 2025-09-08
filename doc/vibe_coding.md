# Vibe coding

* Globally Github copilot is able to generate a working code.

* Global feeling is that it is slow for easy (for a human) requests but relatively  for semi complex requests. Sometimes really slow even for simple prompts. I assume that it was rather a server workload issue than anything else. It is quite impressive and correct to generate a project structure.

* It is not able to handle complex requests, the global request to generate a convertor from an input and output exemple failed. It was easy to check that the generated output was totally different from the requested one, but it provided an answer anyway, even if it often generate test for its code.

* By mistake I made a request related to this project in a totally different one. The AI tried to do something even if it was obvious that the project had nothing to do with the request.

* It does not really learn from previous prompts. When working on a limited portion of code on a project, a human learns and becomes more an more efficient. The AI not. Code analysis to find where to change the code is done over and over. For exemple, if you ask AI to change the color of a button, it has to analyze the code to find where it is handled. If you change your mind and ask for a different color, the analysis is done again. 

* The quality of the code is really medium. It is not really bad code, but obvious optimisations are often missed. It is important to keep the code base minimal for a feature or a project. Maintenance cost are often proportional to the size of the code. When not explicitly requested, the AI generate the same code again and again and often miss the fact that a function with parameters could be used. In the current state of the art, it could quickly becomes an issue for medium and big projects. It would need more investigation but I would not be surprised by projects becoming two or three times bigger than the same ones controlled by human beings.

* Temporary conclusion: AI is currently a goodwill assistant rather dumb, often useful and helping but requesting constant supervision. It cannot be thrusted even on simple tasks.