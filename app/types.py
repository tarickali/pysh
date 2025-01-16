__all__ = ["Command", "Arg", "File", "Mode", "Stream", "IStream", "OStream", "EStream"]

Command = str
Arg = str
File = str
Mode = str
Stream = tuple[File, Mode]
IStream = OStream = EStream = Stream
