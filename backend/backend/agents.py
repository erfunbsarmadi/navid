# backend/agents.py
bull_prompt = build_prompt('bull', ticker, ctx_text)
bear_prompt = build_prompt('bear', ticker, ctx_text)
bull_out = call_llm_system(bull_prompt)
bear_out = call_llm_system(bear_prompt)


# 4) Trader synthesis
synth_prompt = build_prompt('synthesizer', ticker, ctx_text, extras={'tech': tech_out, 'news': news_out, 'bull': bull_out, 'bear': bear_out})
synth_out = call_llm_system(synth_prompt)


# 5) Risk check (simple rule-based + LLM summary)
risk_prompt = build_prompt('risk', ticker, ctx_text, extras={'synth': synth_out})
risk_out = call_llm_system(risk_prompt)


# Return structured payload (raw LLM outputs included for audit)
return {
'ticker': ticker,
'technical': tech_out,
'news': news_out,
'bull': bull_out,
'bear': bear_out,
'synth': synth_out,
'risk': risk_out,
}




def build_context_text(ticker, ctx):
# ctx contains last close, indicators, etc.
lines = [f"Ticker: {ticker}", f"Last Close: {ctx.get('last_close')}"]
for k,v in ctx.items():
lines.append(f"{k}: {v}")
return "\n".join(lines)




def build_prompt(role, ticker, context_text, extras=None):
# Read prompt templates from prompt_bank.md using markers like <!--PROMPT:technical-->
pb = PROMPT_BANK.read_text()
marker = f"<!--PROMPT:{role}-->"
if marker in pb:
start = pb.index(marker) + len(marker)
end_marker = "<!--PROMPT:END-->")
end = pb.index(end_marker, start)
template = pb[start:end].strip()
# interpolate simple variables
template = template.replace("{TICKER}", ticker).replace("{CONTEXT}", context_text)
if extras:
for k,v in extras.items():
template = template.replace(f"{{{k}}}", str(v))
return template
else:
# fallback generic
return f"You are a {role} analyst. Context:\n{context_text}\nAnswer briefly."
