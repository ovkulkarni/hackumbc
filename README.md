## Inspiration

When you split purchases with other people, it's hard to calculate the exact amount of money that each person owes, and people tend to forget who and how much they owe after a while.

## What it does

Cash In! lets you take a picture of a receipt and scans it for items, which are then made into a list in which you can select which person that was bought for. It keeps track of who owes another person and how much they owe. It also keeps an image of the original receipt so you can can view it at a later time.

## How I built it

Cash In! was built using the `Django web framework in Python`. The front-end is `HTML5` and `CSS3` with the `Bootstrap CSS Framework`. All data is stored in a `sqlite3` database.

## Challenges I ran into

- Making sure users can only see what they need to
- Finding a good way to analyze the text that came from the tesseract output
- Submitting a receipt by taking a picture

## Accomplishments that I'm proud of

- Writing this in 24 hours 
- Having OCR that works often
- Building a Django app from scratch
- Making it (somewhat) extensible

## What I learned

- Tesseract
- OCR
- Django
- SQL
- HTML
- CSS
- Javascript

## What's next for Cash In!

We want to add a way to make payments quickly and securely between users. We also want to improve the OCR by giving it more training. One thing we may want to add in the future is support for purchases that don't come with receipts such as online purchases.
