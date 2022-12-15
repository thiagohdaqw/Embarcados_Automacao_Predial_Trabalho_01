from dataclasses import dataclass, field
from collections import deque
from typing import Optional

@dataclass
class Room:
	name:				str

	temperature: 		Optional[float] = field(default=None)
	humidity:			Optional[int]   = field(default=None)

	persons: 			int = field(default=0)
	
	alarm:			  	bool	= field(default=False)
	lamp01:				bool	= field(default=False)
	lamp02:				bool	= field(default=False)
	projector:			bool	= field(default=False)
	air_conditioning:   bool	= field(default=False)
	
	door:				bool	= field(default=False)
	smoke:				bool	= field(default=False)
	window:				bool	= field(default=False)
	presence:			bool	= field(default=False)

	message_queue:  deque	= field(default_factory=deque)
