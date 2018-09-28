from django.shortcuts import render, redirect

from resumen.models import Debate
from debate.models import Position, Argument, Rate, Counterargument, PrivateMembers, Visit
from perfil.models import Profile, Notification
from debate.forms import newArgForm1,newArgForm0, newCounterargForm, newReportReasonForm

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import *
import itertools
import json
import datetime
import pytz

##@brief Funcion que showDebate el debate
##@param request solicitud web
##@param id_debate id del debate solicitado por la url dinamica
##@return render redirecciona a "Debate" si el debate esta abierto y "debate_cerrado" si no
##@warning Login is required
@login_required
def showDebate(request, id_debate): #debate_id
	debate = Debate.objects.get(id_debate= id_debate)
	visits = visitCount(debate, request.user)
	if request.method == 'POST':
		#solicitud de rateArg un argument
		if 'id_arg' in request.POST:
			respuesta = rateArgument(request)
			return HttpResponse(respuesta)
		#solicitud de publicar un contraargumento a favor
		if 'counterargument0' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argument0")
			return redirect(showDebate,id_debate)
		#solicitud de publicar un contraargumento en contra
		if 'counterargument1' in request.POST:
			counterarg = newCounterargument(request, id_debate, "id_argument1")
			return redirect(showDebate,id_debate)
		#solicitud de eliminar un argument
		if 'id_arg_delete' in request.POST:
			id_debate = deleteArgument(request)
			return redirect(showDebate,id_debate)
		#solicitud de reportar un debate
		if 'report_debate' in request.POST:
			report = reportMessage(request, 'debate')
			return redirect(showDebate,id_debate)
		#solicitud de reportar un argumento
		if 'report_argument' in request.POST:
			report = reportMessage(request, 'argument')
			return redirect(showDebate,id_debate)

	owner_user_id = debate.id_user_id #user owner
	owner_user = User.objects.get(id= owner_user_id)
	counterarg_num = debate.counterargs_max
	args_num = debate.args_max
	change_position_num = debate.position_max
	counterarg_type = debate.counterargs_type
	try:
		owner_profile = Profile.objects.get(user= owner_user)
		owner_profile = owner_profile.alias
	except:
		owner_profile = 'username'

	usuario_actual_alias = Profile.objects.get(user= request.user)
	actual_user = request.user

	infavor_arguments = Argument.objects.filter(id_debate_id= id_debate, position= 1)
	against_arguments = Argument.objects.filter(id_debate_id= id_debate, position= 0)
	infavor_args_list = argumentData(infavor_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = argumentData(against_arguments, request.user.id, counterarg_num, id_debate)
	against_args_list = sorted(against_args_list, key=lambda rate: rate['rate'], reverse=True)
	infavor_args_list = sorted(infavor_args_list, key=lambda rate: rate['rate'], reverse=True)

	actual_usr_args_num = Argument.objects.filter(id_debate_id= id_debate, id_user_id=request.user ).count()
	if actual_usr_args_num < args_num:
		can_argue = True
	else:
		can_argue = False

	try:
		actual_user_position = Position.objects.get(id_user_id= actual_user.id, id_debate_id=id_debate)
		position_exist = True
		change_position = actual_user_position.count_change
	except:
		actual_user_position = "No definido"
		position_exist = False
		change_position = 0

	if change_position < change_position_num:
		can_change_position = True
	else:
		can_change_position = False
	counterarg_target = "Ambos"
	if position_exist:
		if actual_user_position.position == 1:
			actual_user_position = "A Favor"
			if counterarg_type == 1:
				counterarg_target = "En Contra"
		else:
			actual_user_position = "En Contra"
			if counterarg_type == 1:
				counterarg_target = "A Favor"
	infavor_position=Position.objects.filter(id_debate_id=id_debate, position=1)
	against_position=Position.objects.filter(id_debate_id=id_debate, position=0)
	infavor_position_num=infavor_position.count()
	against_position_num=against_position.count()
	if (int(against_position_num+infavor_position_num)==0):
		against_percent=0
		infavor_percent=0
	else:
		infavor_percent = round(float(infavor_position_num) / float(against_position_num+infavor_position_num),3)*100
		against_percent = round(float(against_position_num) / float(against_position_num+infavor_position_num),3)*100

	total_positions = Position.objects.all().order_by('-date')

	position_date = Position.objects.filter(id_debate_id = id_debate).values("date")
	position_date_group = itertools.groupby(position_date, lambda record: record.get("date").strftime("%Y-%m-%d"))
	temp = 0
	positions_by_day = [[debate.date.strftime("%Y-%m-%d"),0]]
	for day,position in position_date_group:
		temp += len(list(position))
		positions_by_day.append([day, temp])
	# positions_by_day = json.dumps(positions_by_day)

	infavor_to_against = 0
	against_to_infavor = 0
	reason_infavor_to_against = []
	reason_against_to_infavor = []
	for i in range (1,4):
		num = Position.objects.filter(id_debate_id=id_debate, position=0, change=i).count()
		reason_infavor_to_against.append(num)
		infavor_to_against += num
	for i in range (1,4):
		num = Position.objects.filter(id_debate_id=id_debate, position=1, change=i).count()
		reason_against_to_infavor.append(num)
		against_to_infavor += num

	debate_members = "publico"
	participate = True
	members_list = []
	if debate.members_type == 1:
		debate_members = PrivateMembers.objects.filter(id_debate_id=id_debate)
		for member in debate_members:
			user = User.objects.get(id=member.id_user_id)
			profile = Profile.objects.get(user_id=user.id)
			members_list.append({'user':user, 'profile':profile, 'type':member.type})

		participate = PrivateMembers.objects.filter(id_debate_id=id_debate,id_user_id=actual_user.id).values('type')

		if len(participate)==0:
			participate = False
			options_owner = []
		elif len(participate)==1:
			type = participate[0]['type']
			if type=='username':
				options_owner=[('username', User.objects.get(id=request.user.id).username)]
			else:
				options_owner=[('alias',Profile.objects.get(user= request.user).alias)]
		else:
			options_owner=[('username', User.objects.get(id=request.user.id).username),
		         		   ('alias',Profile.objects.get(user= request.user).alias)]

	else:
		options_owner=[('username', User.objects.get(id=request.user.id).username),
		         ('alias',Profile.objects.get(user= request.user).alias)]

	max_length = Debate.objects.get(id_debate=id_debate).length
	arg_form0 = newArgForm0(owner=options_owner,max_length=max_length)
	arg_form1 = newArgForm1(owner=options_owner,max_length=max_length)
	counterarg_form = newCounterargForm(owner=options_owner,max_length=max_length)
	report_form = newReportReasonForm()

	data = {'debate': debate,
		'owner_user': owner_user,
		'user': actual_user,
		'owner_profile': owner_profile,
		'actual_user_position': actual_user_position,
		'infavor_args_list': infavor_args_list, 'against_args_list': against_args_list,
		'can_argue': can_argue, 'p_post': can_change_position,
		'infavor_position_num': infavor_position_num, 'against_position_num': against_position_num,
		'infavor_percent': infavor_percent, 'against_percent': against_percent,
		'infavor_to_against':infavor_to_against, 'against_to_infavor':against_to_infavor,
		'reason_infavor_to_against':reason_infavor_to_against, 'reason_against_to_infavor':reason_against_to_infavor,
		'counterarg_num':counterarg_num, 'arg_form1':arg_form1,
		'arg_form0':arg_form0,'counterarg_form':counterarg_form,
		'participate': participate, 'debate_members': members_list, 'counterarg_type': counterarg_type,
		'counterarg_target': counterarg_target, 'visits': visits, 'positions_by_day':positions_by_day,
		'report_form':report_form}
	return render(request, 'debate.html', data)

def argumentData(arguments, actual_user, counterarg_num, id_debate):
	args_list = []
	for arg in arguments:
		counterargs = Counterargument.objects.filter(id_argument_id= arg.id_argument)
		counterargs_actual_user_num = Counterargument.objects.filter(id_user_id=actual_user, id_argument_id= arg.id_argument).count()
		counterargs_list = []
		can_counterarg = True
		for counterarg in counterargs:
			id = counterarg.id_counterarg
			text = counterarg.text
			owner = User.objects.get(id=counterarg.id_user_id)
			if counterarg.owner_type == "alias":
				alias = Profile.objects.get(user= owner)
				owner = alias.alias
			else:
				owner = owner.username
			counterargs_list.append({'text': text, 'owner': owner,
									'id': id, 'id_owner': counterarg.id_user_id,
									'owner_type': counterarg.owner_type})
			if counterargs_actual_user_num < counterarg_num:
				can_counterarg = True
			else:
				can_counterarg = False
		owner_arg = User.objects.get(id= arg.id_user_id)
		owner_arg_id = owner_arg.id
		if (arg.owner_type == "alias"):
			owner_profile = Profile.objects.get(user=owner_arg)
			owner_arg = owner_profile.alias
		try:
			rate = Rate.objects.get(id_argument_id= arg.id_argument, id_user_id = actual_user, rate_type="positive")
			positive_rate_exist = "si"
		except:
			positive_rate_exist = "no"
		try:
			rate = Rate.objects.get(id_argument_id= arg.id_argument, id_user_id = actual_user, rate_type="negative")
			negative_rate_exist = "si"
		except:
			negative_rate_exist = "no"
		exist_rate=[positive_rate_exist,negative_rate_exist]
		positive_rate = Rate.objects.filter(id_argument_id= arg.id_argument, rate_type="positive").count()
		negative_rate = Rate.objects.filter(id_argument_id= arg.id_argument, rate_type="negative").count()
		total_rate = positive_rate - negative_rate
		arg.score = total_rate
		arg.save()
		position_owner_arg = Position.objects.get(id_user_id= arg.id_user_id, id_debate_id=id_debate).position
		args_list.append({'text': arg.text, 'owner_arg': owner_arg, 'rate': total_rate,
							'id_arg': arg.id_argument, 'exist_rate': exist_rate, 'owner_arg_id': owner_arg_id, 'counterargs': counterargs_list,
							'can_counterarg': can_counterarg, 'owner_type':arg.owner_type})
	return args_list

##@brief Funcion que guarda el arguments del user de un argument.
##@param request solicitud web, entrega los datos del user actual
##@return id_debat para redireccional a la vista "showDebate" con este id de debate
##@warning Login is required
@login_required
def newCounterargument(request,id_debate, id_argument):
	if request.method == "POST":
		id_arg = request.POST[id_argument]
		counterarg_form = newCounterargForm(request.POST, owner=0, max_length=0)
		if counterarg_form.is_valid():
			post = counterarg_form.save(commit=False)
			post.id_user_id = request.user.id
			post.id_argument_id = id_arg
			post.save()
		updateReputation(request.user.id, 3)
	return counterarg_form

def updateReputation(id_usr, score):
    profile = Profile.objects.get(user_id=id_usr)
    reputation = profile.reputation + score
    profile.reputation = reputation
    profile.save()

##@brief Funcion que guarda la valoracion del user al argument
##@param request solicitud web, entrega los datos del user actual
##@return respuesta se ingresa en el HttpResponse para indicar la valoracion actualizada del argument
##@warning Login is required
@login_required
def rateArgument(request):
	rate_argument= request.POST['id_arg']
	rate=request.POST['option_rate']
	if rate == "positive":
		score = 4
	elif rate =="negative":
		score = -2
	elif rate =="null-positive":
		score = -4
	elif rate =="null-negative":
		score = 2
	try:
		rate_post = Rate.objects.get(id_argument_id=rate_argument, id_user_id=request.user.id);
		actual_rate = rate_post.rate_type
		if rate == "positive" or rate == "negative":
			if actual_rate == "positive":
				score -= 4
			elif actual_rate == "negative":
				score += 2
		rate_post.rate_type = rate
	except:
		rate_post = Rate(id_argument_id=rate_argument, id_user_id=request.user.id, rate_type=rate)
	rate_post.save()
	id_owner_arg = Argument.objects.get(id_argument=rate_argument).id_user_id
	updateReputation(id_owner_arg, score)
	positive_rate = Rate.objects.filter(id_argument_id= rate_argument, rate_type="positive").count()
	negative_rate = Rate.objects.filter(id_argument_id= rate_argument, rate_type="negative").count()
	total_rate = positive_rate - negative_rate
	return(total_rate)

def deleteArgument(request):
	id_arg = request.POST['id_arg_delete']
	id_deb=request.POST['id_deb_arg_eliminar']
	arg = Argument.objects.get(pk=id_arg)
	arg.delete()
	updateReputation(request.user.id, -3)
	return (id_deb)

def reportMessage(request, type):
	actual_user = request.user
	reason = request.POST['reason']
	if type=='debate':
		id_debate = request.POST['id_deb']
		debate = Debate.objects.get(id_debate=id_debate)
	elif type=='argument':
		id_arg = request.POST['id_report_arg']
		arg = Argument.objects.get(pk=id_arg)
		debate = Debate.objects.get(pk=arg.id_debate_id)
	report_form = newReportReasonForm(request.POST)
	if report_form.is_valid():
		post = report_form.save(commit=False)
		post.owner = request.user
		post.debate = debate
		post.type = type
		if type=="argument":
			post.argument = arg
		post.save()
	# updateReputation(request.user.id, 3)
	return report_form


def readNotification(request, id_debate, id_notification):
	notification = Notification.objects.get(id=id_notification)
	notification.state = 1
	notification.save()
	return redirect(showDebate,id_debate)

def visitCount(debate, user):
	utc=pytz.UTC
	try:
		visit = Visit.objects.get(id_debate=debate, id_user_id=user.id)
		delta = visit.date + timedelta(minutes=30)
	except:
		visit = Visit.objects.create(id_debate=debate, id_user_id=user.id)
		delta = utc.localize(visit.date) + timedelta(minutes=30)
	ahora = utc.localize(datetime.datetime.today())
	if delta <= ahora:
		visit.num = visit.num + 1
		visit.date = ahora
		visit.save()
	total = Visit.objects.filter(id_debate=debate).aggregate(Sum('num'))
	return total.values()[0]
