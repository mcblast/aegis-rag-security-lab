# AI Security Policy

AI applications must separate trusted system instructions from untrusted user content and retrieved document content. Retrieved context should be treated as data, not as authority over the system.

Prompt injection occurs when malicious input attempts to override developer instructions, reveal hidden prompts, bypass policy, or manipulate downstream actions. Indirect prompt injection can enter through documents, emails, tickets, web pages, or any external content placed into model context.

Baseline Phase 01 does not defend against prompt injection. Later phases will introduce prompt boundary enforcement, context sanitization, output validation, and adversarial evaluation.
