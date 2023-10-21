import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket
from .form import CreateTicketForm, UpdateTicketForm
from users.models import User

''' FOR BOTH ENGINEERS AND CUSTOMERS '''
# view ticket details
@login_required
def ticket_details(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by)
    tickets_per_user = t.created_by.all()
    context={'ticket':ticket, 'tickets_per_user': tickets_per_user}
    return render(request, 'ticket/ticket_details.html', context)

''' FOR CUSTOMERS '''

# creating a ticket
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Your ticket has been successfully created! An engineer would be assigned soon!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong! Check your inputs')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)
    
# updating a ticket
@login_required
def update_ticket(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved and request.user.is_customer:        
        if request.method == 'POST':
            form = CreateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request,'Your ticket has been successfully updated!')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong! Check your inputs')
                # return redirect('create-ticket')
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {'form': form}
            return render(request, 'ticket/update_ticket.html', context)
    else:
        messages.warning(request,'You cannot update a closed ticket')
        return redirect('dashboard')

# viewing all tickets
@login_required
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request, 'ticket/all_tickets.html', context)


''' FOR ENGINEERS '''

# view ticket queue
@login_required
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request,'ticket/ticket_queue.html', context=context)

# accept a ticket from the queue
@login_required
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted. Please resolve at the earliest!')
    return redirect('workspace')

# close a ticket 
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.closed_date = datetime.datetime.now()
    ticket.is_resolved = True
    ticket.save()
    messages.info(request, 'Ticket has been resolved. Thank You so much!')
    return redirect('ticket-queue')

# ticket engineer is working on
@login_required 
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False).order_by('-date_created')
    context={'tickets':tickets}
    return render(request,'ticket/workspace.html',context)

# all closed/resolved tickets
@login_required
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True).order_by('-date_created')
    context={'tickets':tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)