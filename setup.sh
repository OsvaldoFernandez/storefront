pip3 install pipenv
pipenv install django #similar to bundler
pipenv shell # activate el url que te dan
#django-admin (similar to rake)
django-admin startproject storefront .

#como usar el bundle install:
pipenv install django-debug-toolbar

# Se usa pyhotn manage.py que es como un alias de django-admin. 
# Es similar a rake. 
# Un proyecto de django puede tener mas de una app (una app sería como una gema)
python manage.py startapp likes     

#Correr el server
python manage.py runserver  

# Acá los contorllers son views.py. Y las views son templates

# Vos definís un esquema en models.py. Para que ese esquema se vea reflejado en migrations, correr:
python manage.py makemigrations  
# Esto crea las migraciones necesarias. si vos cambiás un field en models.py te crea la migration que te lo hace. 

# Para correr las migrations
python manage.py migrate 

# Para rollbackearlas, ir a una específica, basado en índice, por ejemplo: 
python manage.py migrate store 0003  

# Si querés popular con un seed, podés generar una migration vacía 
python manage.py makemigrations store --empty
# Recordar que tiene que tener un UP and DOWN como buena práctica. 

# IMPORTANTE: para SQL server hay que reiniciar las secuencias o sino no sabe cómo storearte la PK empieza por 1 
python manage.py sqlsequencereset store

# ORM OR: queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
# ORM NOT: queryset = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))
# ORM: Comparar dos fields de la misma tabla queryset = Product.objects.filter(inventory=F('collection_id'))
# ORM: queryset = Product.objects.values('id','title') ES UN PLUCK
# ORM: queryset = Product.objects.only('id','title') Devuelve instancias reducidas del objeto. OJO CON LAS N QUERIES. Defer es lo opuesto a only
# ORM: queryset = Product.objects.select_related('collection').all() es el INCLUDE de activeRecord
# ORM: queryset = Product.objects.prefetch_related('promotions').all() es el INCLUDE en ManyToMany promotion_set si es onetoMany
# ORM: combinado: queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
# ORM: Aregate: Min Max Count Avg
# ORM: Annotate: es como el select de activerecord, util para agregar campos desde sql. 
# ORM: Func object es medio una magia funcional: annotate(full_name=Func(F('first_name'), Value(''), F('last_name'), function='CONCAT')) donde CONCAT es la target function

# Genérico (para los tags): content_type = ContentType.objects.get_for_model(Product). Luego filtrar tagged items con exacto content_type y object_id
# Delecator class TaggedItemManager(models.Manager): (y métodos). Asignar TaggedItems.objects a ese Manager
# Django cachea. Pero tenés que listarlos todos primero

# TRICKY: 
# collection = Collection(pk=11) CREA un objeto vacío con PK 11, a la hora de guardar sobreescribe el 11 como update. Posible data loss
# collection = Collection.objects.get(pk=11) trae en memoria el objeto entero. Save() no tiene un data loss

# PARA CUSTOM QUERIES 
# with connection.cursor() as cursor: cursor.execute()

# python manage.py createsuperuser    
# actualizar seqs en pgsql

# CONTEXT OBJECT: le da datos adicionales al serializer, Ver el caso de reviews que siempre queremos que tome el product de la URL

