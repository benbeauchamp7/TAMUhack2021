v = "$AAL $ACB $AG $AMC $AMD $BB $BBBY $BYND $CCIV $CLOV $CRIS $GM $GME $HIMS $INO $IPOE $IPOF $KOSS $MRNA $NCTY $NVAX"
tickers = ["$MSR", "$AMC"]
for word in v.split(' '):
  for t in tickers:
    if word.lower() == t.lower():
      print(word)