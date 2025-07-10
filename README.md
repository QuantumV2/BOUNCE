# BOUNCE
## Overview
BOUNCE is an two-dimensional esoteric programming language where the Instruction Pointer is always moving diagonally and can bounce off "#" characters and the boundaries of the program.
## Usage
Install the requirements:
<pre>
pip install -r requirements.txt
</pre>
Run main.py
<pre>
py main.py examples\factorial.bnc
</pre>
Disable self.debugprinting in interpreter.py if you do not want to see the IP bouncing around

## Instructions
<pre>
+,-,*,/,% - Arithmetic operations. First argument is the second to last element on the stack and the second argument is the last element on the stack.

Stack ops:
: - Duplicate the top of the stack.
~ - Swap two top elements on the stack.
. - Pop and print as number.
, - Pop and print as a character.
$ - Pop.
& - Input integer.
@ - Rotate three top elements on the stack (abc) -> (cab).
^ - Rotate the entire stack (abcdef) -> (fabcde).
v - Push the stack length onto the stack.

Walls:
# - Wall. The IP bounces off.
= - Becomes a wall when touched by the IP.
" - Becomes a wall when the IP attempts to bounce on it.
? - Acts like a wall if the top of the stack is not 0.

Other:
! - End the program.
</pre>