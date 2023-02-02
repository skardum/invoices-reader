string = "☺◄Golden Hands Est.☻310597963800003♥↓2022-08-23T09:12:56+03:00♦11500.0♣♠1500.0"

name_of_seller = string.split("☺◄")[1].split("☻")[0]
vat_number = string.split("☺◄")[1].split("☻")[1].split("♥↓")[0]
date_and_time = string.split("☺◄")[1].split(
    "☻")[1].split("♥↓")[1].split("♦")[0]
total_amount = float(string.split("☺◄")[1].split(
    "☻")[1].split("♥↓")[1].split("♦")[1].split("♣♠")[0])
vat_amount = float(string.split("☺◄")[1].split(
    "☻")[1].split("♥↓")[1].split("♦")[1].split("♣♠")[1])

print("Name of Seller:", name_of_seller)
print("VAT Number:", vat_number)
print("Date and Time:", date_and_time)
print("Total Amount:", total_amount)
print("VAT Amount:", vat_amount)


def remove_non_printable(text):

    chars_to_remove = "?,☺,☻,♥,♦,♠,♣,§,¶,\x01,\x02,\x03,\x04,\x05,\x0e,\x1e,\x13,\x0f,\x14,\x15,\x06,\x07,\x19,\x08,\t,.00"
    for char in chars_to_remove:
        text = text.replace(char, ",")
    # Remove "," from the beginning of the string
    if len(text) > 0 and text[0] == ",":
        text = text[1:]
    # Remove duplicate ","
    text = ','.join(text.split(","))
    result = [x for x in text.split(",") if x]
    return result
