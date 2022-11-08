import re
line="""@{name:ABC,type:Model}@234567u8iopoiuytrewqqwertyuiolkjhgf@{name:ABC,type:Model2}@234567u8iopoiuytrewqd@{name:ABC,type:Model}@23e4rtyujk"""
input=str(line).strip().replace("\n","").replace(" ","")
print("input:"+str(input).strip())
pattern = re.compile(r"@\{.*?\}@")
result=pattern.search(str(input))
print(result.groups())

result=pattern.findall(str(input))
print(result)

