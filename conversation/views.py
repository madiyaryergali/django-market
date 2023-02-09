from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from item.models import Item
from conversation.models import Conversation
from conversation.forms import ConversationMessageForm

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk = item_pk)

    if item.created_by==request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id ])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id) 

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        print(item_pk)
        if form.is_valid():
            conversation = Conversation.objects.create(item = item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            print(item_pk)
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('dashboard:index')
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id ])

    return render(request, 'conversation/inbox.html',{
        'conversations': conversations,
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id ]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
    })
