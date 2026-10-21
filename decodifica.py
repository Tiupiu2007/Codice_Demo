
import base64

messaggio = (
    "UGJ6Y3l2enJhZ3YgY3JlIHJmZnJlciBuZWV2aW5nYiBzdmEgZGh2ISBZbiBmc3ZxbiBhYmEgcG56b3ZuLCB5cnR0diBuZ2dyYWduenJhZ3IgdnkgYWJmZ2ViIGZ2Z2IgciBjcmFmbiBucSBoYSduY2N5dnBubXZiYXIgdmEgeXZhcm4gcGJhIHluIGFiZmdlbiB6dmZmdmJhciByIGNlYmluIG4gZml2eWhjY25lYXIgaGFuIHFyemIgYiBmYnluenJhZ3IgdnkgcGJhcHJjZy4gVmFpdm55biB2YWZ2cnpyIG55IGdoYiBwaGVldnBoeWh6IHF2ZXJnZ256cmFnciBueSBhYmZnZWIgZXJjbmVnYiBncnBhdnBiLCBuIHFyaUBudmVjdnoucGJ6IHBiYSBidHRyZ2diOiBPdnQgUW5nbiBRcmlyeWJjcmUgLSBGc3ZxbiAy=="
)

def ruota_cesare(testo, rotazione):
    risultato = ""

    for carattere in testo:
        if "a" <= carattere <= "z":
            risultato += chr((ord(carattere) - ord("a") + rotazione) % 26 + ord("a"))
        elif "A" <= carattere <= "Z":
            risultato += chr((ord(carattere) - ord("A") + rotazione) % 26 + ord("A"))
        else:
            risultato += carattere

    return risultato

testo = base64.b64decode(messaggio).decode("utf-8")

for rotazione in range(1, 14):
    risultato = ruota_cesare(testo, rotazione)
    print(f"\nROT{rotazione}: {risultato}")

print("\nTesto Decodificato:")
print(ruota_cesare(testo, 13))
