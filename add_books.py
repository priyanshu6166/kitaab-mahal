import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitaab_mahal.settings')
django.setup()

from books.models import Book

# List of books to add
books_data = [
    {
        'title': 'HARRY POTTER',
        'description': 'The magical journey of a young wizard and his friends at Hogwarts School of Witchcraft and Wizardry.',
        'cover_image': 'static/harrpoter.jpg',
        'pdf_file': 'static/Harry Potter and the Sorcerers Stone.pdf',
    },
    {
        'title': 'RICH DAD POOR DAD',
        'description': 'A personal finance book that emphasizes financial education and building wealth through investments.',
        'cover_image': 'static/rich dad.webp',
        'pdf_file': 'static/richdad poor dad.pdf',
    },
    {
        'title': 'A LITTLE LIFE',
        'description': 'A novel that follows four college friends in New York City, focusing on Jude St. Francis and his traumatic past.',
        'cover_image': 'static/little life.webp',
        'pdf_file': 'static/A little Life - Hanya Yanagihara.pdf',
    },
    {
        'title': 'WHITE NOISE',
        'description': 'A postmodern novel that explores themes of death, consumerism, and the fear of death in modern society.',
        'cover_image': 'static/whitw noise.webp',
        'pdf_file': 'static/WHITE NOISE.pdf',
    },
    {
        'title': 'AMERICAN PSYCHO',
        'description': 'A psychological thriller that follows the life of Patrick Bateman, a wealthy investment banker who leads a double life as a serial killer.',
        'cover_image': 'static/amrican.jpg',
        'pdf_file': 'static/amrican.pdf',
    },
    {
        'title': 'THE LINE OF BEAUTY',
        'description': 'A novel that follows the life of Nick Guest, a young gay man who moves into the home of a wealthy Conservative MP in 1980s London.',
        'cover_image': 'static/the line of beauty.webp',
        'pdf_file': 'static/The Line of Beauty [EnglishOnlineClub.com].pdf',
    },
    {
        'title': 'THE GOD OF SMALL THINGS',
        'description': 'A novel that tells the story of fraternal twins whose lives are destroyed by the "Love Laws" that lay down "who should be loved, and how."',
        'cover_image': 'static/the good of small thing.jpg',
        'pdf_file': 'static/The God of Small Things.pdf',
    },
    {
        'title': 'JANE EYRE',
        'description': 'A novel that follows the experiences of its eponymous heroine, including her growth to adulthood and her love for Mr. Rochester.',
        'cover_image': 'static/jane eyre.jpg',
        'pdf_file': 'static/Jane Eyre.pdf',
    },
    {
        'title': 'DAVID COPPERFIELD',
        'description': 'A novel that follows the life of David Copperfield from childhood to maturity, chronicling his personal growth and development.',
        'cover_image': 'static/david.webp',
        'pdf_file': 'static/David Copperfield.pdf',
    }
]

# Add books to database
for book_data in books_data:
    # Create book object
    book = Book.objects.create(
        title=book_data['title'],
        description=book_data['description']
    )
    
    # Set cover image
    with open(book_data['cover_image'], 'rb') as img:
        book.cover_image.save(os.path.basename(book_data['cover_image']), img, save=True)
    
    # Set PDF file
    with open(book_data['pdf_file'], 'rb') as pdf:
        book.pdf_file.save(os.path.basename(book_data['pdf_file']), pdf, save=True)
    
    print(f"Added book: {book.title}")

print("All books have been added successfully!") 