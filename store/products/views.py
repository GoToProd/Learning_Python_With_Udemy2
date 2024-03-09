from django.shortcuts import render


def index(request):
    
    context = {
        'title': 'Store',
        'is_promoution': True,
    }
    
    return render(request, 'products/index.html', context)


def products(request):
    
    context = {
        'title': 'Store - каталог',
        'products': [
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'name': 'Худи черного цвета ткань для свитшота',
                'price': 6900,
                'description': 'Мягкая ткань для свитшота от оригинального бренда',
            },
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'name': 'блфоывлфыов фловафыолафыва 2!!!!!',
                'price': 6900,
                'description': 'влдыжораимыдиарафдвыаио вылдатоимыфвдтиомтлфылвмдтлд ывждлтмдылвятмаыфлд',
            },
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'name': 'бвьмлдаивотляидлавит ывалтдвылатид 3',
                'price': 6900,
                'description': 'фылдоавмиодатмиоываоямадиото лдвти длатвфдлияваытдлитдв длватидылявты',
            }
        ],
    }
    
    return render(request, 'products/products.html', context)