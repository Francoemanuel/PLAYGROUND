
**Crear registros con create**

    Author.objects.create(name="George Orwell", birth_date="1903-06-25")

**Crear registros con save**

    rowling = Author(name="J.K. Rowling", birth_date="1965-07-31") rowling.save()

**Registros relacionados con Foreign Key**

    orwell = Author.objects.get(name="George Orwell") Book.objects.create( title="1984", publication_date="1949-06-08", author=orwell )
   
 **Crear registros en lote**
 

    cuellar = Author.objects.get(name="Ricardo Cuellar") 
    Book.objects.bulk_create([ 
    Book(title="Me enammore de su software", publication_date="1985-09-05", author=Author.objects.get(name=cuellar)), 
    Book(title="Harry Potter y el prisionero de Ecatepec", publication_date="1997-06-26", author=Author.objects.get(name=cuellar)), 
    ])
  
  **Comparativas de rendimiento para crear en lote .save() vs bulk_create()**

	Usando save:
	start = time.time() 
	for i in range(1000): 
		book = Book( title=f"Libro lento {i}", publication_date="2000-01-01", author=author, pages=100, isbn=f"123456{i}" ) 
		book.save() 
	end = time.time() 
	print(f"Tiempo usando .save(): {end - start:.2f} segundos")


    Usando bulk_create():
    start = time.time() 
    books = [] 
    for i in range(1000): 
	    books.append(Book( title=f"Libro rápido {i}", publication_date="2000-01-01", author=author, pages=250, isbn=f"98765{i}" )) 
	
	Book.objects.bulk_create(books) 
	end = time.time() 
	print(f"Tiempo usando bulk_create(): {end - start:.2f} segundos")


**Usando get or create y update or create**

    Author.objects.get_or_create(name="George Orwell", defaults={"birth_date": "1903-06-25"}) 
    Book.objects.update_or_create( title="Harry Potter y la piedra filosofal", defaults={ "publication_date": "1997-06-26", "author": rowling } )

**Consultas básicas**

    Book.objects.all() # Todos los libros
    Book.objects.get(id=1) # Un libro por ID (lanza error si no existe) 
    Book.objects.first() # Primer libro 
    Book.objects.last() # Último libro

**Ordenar objetos**

    Book.objects.order_by('title') 
    Book.objects.order_by('-title') 
    Book.objects.order_by('title') 
    Book.objects.order_by('author','title') 
    Book.objects.order_by('?')

**Filtrando objetos y obtener SQL**

    books = Book.objects.filter(title="Harry Potter y el prisionero de Ecatepec") 
    #Ahora para obtener el query usamos 
    print(books.query)

**Filtros usando campos de búsqueda (sensitive e insensitive)**

    Book.objects.filter(title="Me enamore de su software") Book.objects.filter(title__exact="me enamore de su software") 
    Book.objects.filter(title__iexact="me enamore de su software") 
    Book.objects.filter(title__contains='Potter') 
    Book.objects.filter(title__icontains='potter') 
    Book.objects.filter(title__istartswith='harry') 
    Book.objects.filter(title__iendswith='ecatepec')
    Book.objects.filter(title__startwith-'Harry').exists()

**Filtrando por rango**

    Book.objects.filter(id__in=[1,10,11,29])
    Book.objects.filter(id__gt=10) 
    Book.objects.filter(id__gte=10)
    Book.objects.filter(id__lt=10) 
    Book.objects.filter(id__lte=10)

**Filtrando por fechas**

    from datetime import date 
    # IMPORTANTE: Si publication_date es una fecha ya no hace falta poner __date
    Book.objects.filter(publication_date__date=date(2025,1,1)) 
    Book.objects.filter(publication_date=date(2025,1,1)) 
    Book.objects.filter(publication_date__year=2025) 
    Book.objects.filter(publication_date__month=6) 
    Book.objects.filter(publication_date__day=11) 
    Book.objects.filter(publication_date__date__gt=date(2010,1,1))


**Encadenamiento de filtros y excluir datos**

    Encadenamiento
    Book.objects.filter(publication_date_lt=date(2001,1,1)).filter(author=1)

    Excluir datos:
    Book.objects.filter(author_id = 2).exclude(title__startswith='Libro')

**Limitando conjunto de consultas**

    Book.object.all()[0:5] Book.object.all()[3:10] 
    # o podemos tambien controlar sobre que queremos traer por ejemlo 
    Book.object.order_by('?')[0]

**Consultas avanzadas Q**

    from django.db.models import Q
    # Libros cuyo título contenga “cien” o “amor” 
    Book.objects.filter(Q(title__icontains="cien") | Q(title__icontains="amor")) 
    # Autores cuyo nombre sea “Gabriel” y cuyo ID sea menor a 5 
    Author.objects.filter(Q(name="Gabriel") & Q(id__lt=5))

**Consultas avanzadas F**

    from django.db.models import F
    Book.objects.filter(pages_read__lt=F('pages_total'))

**Actualización de datos**

    Actualización individual:
    author = Author.objects.get(name="Gabriel García Márquez") 
    author.name = "Gabo Márquez" 
    author.save()

    Actualización por lotes:
    Book.objects.filter(author__name="J.K. Rowling").update(title="Título actualizado")
    

**Eliminación de datos**

    Eliminar registro individual:
    book = Book.objects.get(title="1984") 
    book.delete()

    Eliminar por lote:
    CUIDADO: Eliminar por lote es peligroso.
    Book.objects.filter(publication_date__year__lt=1950).delete()

**Comportamientos del on_delete**

`CASCADE`

Si borras el autor, se borran también sus libros (heredados).

`PROTECT`

Impide borrar si hay libros vinculados.

`SET_NULL`

Pone `NULL` en `author` si se elimina el autor.

`SET_DEFAULT`

Usa un valor por defecto.

`DO_NOTHING`

No hace nada (puede lanzar error de integridad referencial).

**Soft Delete **

    class Book(models.Model): 
	    title = models.CharField(max_length=200) 
		is_active = models.BooleanField(default=True)

    Book.objects.filter(is_active=True)

**Agreggates**
Recuerda que se usa para obtener un valor único y global.
    
    from django.db.models import Count, Avg, Sum, Min, Max 
    Book.objects.aggregate(total_libros=Count('id'))

**Annotations**
Recuerda que se usa para agregar una columna virtual a cada registro

    from django.db.models import Count 
    authors = Author.objects.annotate(num_books=Count('book'))
    for author in authors: 
	    print(f"{author.name} tiene {author.num_books} libros")

**Transacciones atómicas**

    from django.db import transaction 
    with transaction.atomic(): 
	    # Todo lo que esté aquí es parte de la misma transacción ...

Ejemplo

    from django.db import IntegrityError 
    from .models import Author, Book 
    try: 
	    with transaction.atomic(): 
		    author = Author.objects.create(name="Autor Ejemplo") 
		    # Esto fallará si el campo obligatorio falta 
		    book = Book.objects.create(title=None, author=author) 
	except IntegrityError: print("Algo salió mal. No se guardó nada.")

