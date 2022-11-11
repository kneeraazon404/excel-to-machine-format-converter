from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files import File
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.views.generic import CreateView

# relative import of forms
# relative import of forms
from course.forms import (
    BrandNameForm,
    MarketIdForm,
    ProfileUpdateForm,
    StoreForm,
    StoreNumberForm,
    UserRegisterForm,
    UserUpdateForm,
    TerminalIdForm,
)
from course.models import MarketId, Store, StoreNumber, TerminalId
from course.utils import generate_machine_data


@login_required
def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES)
        uploaded_file = request.FILES["uploaded_file"]

        if form.is_valid():
            form.instance.user = request.user
            brand_name = form.cleaned_data["brand_name"]
            market_id = form.cleaned_data["market_id"]
            store_number = form.cleaned_data["store_number"]
            cash_registery = form.cleaned_data["terminal_id"]
            uploaded_file = form.cleaned_data["uploaded_file"]

            instance = Store(
                uploaded_file=uploaded_file,
                user=request.user,
                brand_name=brand_name,
            )

            generate_machine_data(
                uploaded_file,
                market_id,
                store_number,
                cash_registery,
            )
            today = datetime.today().strftime("%Y%m%d%H")
            today_new = datetime.today().strftime("%Y%m%d%H%M%S")
            with open(f"{today}.SALES.{market_id}", "rb") as txt_file:
                instance.converted_file.save(
                    f"{today_new}.SALES.{market_id}", File(txt_file)
                )
                instance.user = request.user
                instance.save()
            # form.save()
            return redirect("dashboard")
    else:
        form = StoreForm()
        context["form"] = form
        return render(request, "store_form.html", context)

    return render(request, "store_form.html")


@login_required
def dashboard(request):
    users = User.objects.all().order_by("-date_joined")
    stores = Store.objects.all().order_by("-created_at")
    return render(request, "dashboard.html", {"users": users, "stores": stores})


# update view for details
@login_required
def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}
    if request.method == "POST":

        # fetch the object related to passed id
        obj = get_object_or_404(Store, id=id)

        # pass the object as instance in form
        form = StoreForm(request.POST or None, instance=obj)

        # save the data from the form and
        # redirect to detail_view
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

        # add form dictionary to context
        context["form"] = form

        return render(request, "update_view.html", context)
    obj = get_object_or_404(Store, id=id)
    form = StoreForm(request.POST or None, instance=obj)
    context["form"] = form
    return render(request, "update_view.html", context)


# delete view for details
@login_required
def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Store, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")

    return render(request, "delete_view.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )
            return redirect("dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "account/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
        messages.success(
            request, f"Your account has been created! You are now able to log in"
        )
        return redirect("dashboard")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "account/profile.html", context)


@login_required
def user_update_view(request, id):
    if request.method == "POST":
        obj = get_object_or_404(User, id=id)
        u_form = UserUpdateForm(request.POST or None, instance=obj)
        if u_form.is_valid:
            u_form.save()
        messages.success(
            request, f"A ccount has been Updated! You are now able to log in"
        )
        return redirect("dashboard")

    else:
        obj = get_object_or_404(User, id=id)

        u_form = UserUpdateForm(request.POST or None, instance=obj)

    context = {"u_form": u_form}
    return render(request, "user_update_form.html", context)


@login_required
def delete_user_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(User, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")

    return render(request, "delete_view.html", context)


class MarketIdCreateView(LoginRequiredMixin, CreateView):
    model = MarketId
    fields = ["market_id"]

    def form_valid(self, form):
        return super().form_valid(form)


class StoreNumberCreateView(LoginRequiredMixin, CreateView):
    model = StoreNumber
    fields = ["store_number"]

    def form_valid(self, form):
        return super().form_valid(form)


class TerminalIdCreateView(LoginRequiredMixin, CreateView):
    model = TerminalId
    fields = ["terminal_id"]

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def add_terminal_id(request):
    if request.method == "POST":
        form = TerminalIdForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("/")
    else:
        form = TerminalIdForm(request.POST)
        return render(request, "create_terminal_id.html", {"form": form})
    form = TerminalIdForm(request.POST)
    return render(request, "create_terminal_id.html", {"form": form})


@login_required
def add_market_id(request):
    if request.method == "POST":
        form = MarketIdForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("/")
    else:
        form = MarketIdForm(request.POST)
        return render(request, "create_market_id.html", {"form": form})
    form = MarketIdForm(request.POST)
    return render(request, "create_market_id.html", {"form": form})


@login_required
def add_store_number(request):
    if request.method == "POST":
        form = StoreNumberForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect("/")
    else:
        form = StoreNumberForm(request.POST)
        return render(request, "create_store_number.html", {"form": form})
    form = StoreNumberForm(request.POST)
    return render(request, "create_store_number.html", {"form": form})


@login_required
def add_brand_name(request):
    if request.method == "POST":
        form = BrandNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = BrandNameForm(request.POST)
        return render(request, "create_new_brand.html", {"form": form})
    form = BrandNameForm(request.POST)
    return render(request, "create_new_brand.html", {"form": form})
