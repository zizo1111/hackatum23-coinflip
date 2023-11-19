from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: X.Org X Server 1.21.1.4
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: X Protocol Version 11, Revision 0
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Current Operating System: Linux CMX50070-101776 5.15.73 #1 SMP PREEMPT Sun May 21 21:05:48 UTC 2023 x86_64
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Kernel command line: BOOT_IMAGE=/boot/vmlinuz root=/dev/sda2 video=eDP-1:d ro
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:  
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Current version of pixman: 0.40.0
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         Before reporting problems, check http://wiki.x.org
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         to make sure that you have the latest version.
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Markers: (--) probed, (**) from config file, (==) default setting,
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         (++) from command line, (!!) notice, (II) informational,
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         (WW) warning, (EE) error, (NI) not implemented, (??) unknown.
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Log file: "/var/log/Xorg.0.log", Time: Thu Nov  9 13:11:42 2023
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Using config directory: "/etc/X11/xorg.conf.d"
Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Using system config directory "/usr/share/X11/xorg.conf.d"
"""
print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))

# import torch
# from transformers import T5Tokenizer, T5ForConditionalGeneration

# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto")

# input_text = """what happens in the following log:

# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: X.Org X Server 1.21.1.4
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: X Protocol Version 11, Revision 0
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Current Operating System: Linux CMX50070-101776 5.15.73 #1 SMP PREEMPT Sun May 21 21:05:48 UTC 2023 x86_64
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Kernel command line: BOOT_IMAGE=/boot/vmlinuz root=/dev/sda2 video=eDP-1:d ro
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:  
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Current version of pixman: 0.40.0
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         Before reporting problems, check http://wiki.x.org
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         to make sure that you have the latest version.
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: Markers: (--) probed, (**) from config file, (==) default setting,
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         (++) from command line, (!!) notice, (II) informational,
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]:         (WW) warning, (EE) error, (NI) not implemented, (??) unknown.
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Log file: "/var/log/Xorg.0.log", Time: Thu Nov  9 13:11:42 2023
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Using config directory: "/etc/X11/xorg.conf.d"
# Nov 09 13:11:42 CMX50070-101776 Xserver[1884]: (==) Using system config directory "/usr/share/X11/xorg.conf.d"
#  """

# input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

# outputs = model.generate(input_ids)
# print(tokenizer.decode(outputs[0]))