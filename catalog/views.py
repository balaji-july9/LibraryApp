from django.views import generic
from .models import Book,Author,BookInstance, Genre
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
    # session management
    num_visits=request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1


    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_visits':num_visits},
    )







class BookListView(generic.ListView):
	model=Book
	paginate_by=1
	def get_queryset(self):
		return Book.objects.filter(title__icontains='c')[:5]
	def get_context_data(self,**kwargs):
		context=super(BookListView,self).get_context_data(**kwargs)
		context['some_data']='this is just some data'
		return context
class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request,pk):
    	try:
        	book_id=Book.objects.get(pk=pk)
    	except Book.DoesNotExist:
        	raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
    	return render(
        	request,
        	'catalog/book_detail.html',
        	context={'book':book_id,}
   			 )

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')