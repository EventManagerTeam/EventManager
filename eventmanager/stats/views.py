from django.shortcuts import render

from events.models import Comment
from events.models import Event

import plotly.offline as opy
import plotly.graph_objs as go

import datetime


def get_statistics(request, slug):

	event = Event.objects.get(slug=slug)
	members = event.team_members.all()

	if request.user in members:
		event_comments = Comment.objects.filter(event=event)
		yesterday = datetime.date.today() - datetime.timedelta(days=1)
		alltime_comments = event_comments.count()
		daily_comments = event_comments.filter(created_at__gt=yesterday).count()

		data = [go.Bar(
			x=['Total', 'Daily'],
			y=[alltime_comments, daily_comments],
			marker=dict(
	        	color=['rgba(50,171,96,1.0)', 'rgba(222,45,38,0.8)'],
	        	line=dict(
		            color='rgb(8,48,107)',
		            width=1.5
	            ),
	        ),
	        textposition = 'auto',
	        opacity=0.8,
		)]

		layout=go.Layout(title="Comments compare",font=dict(family='Courier New, monospace', size=20, color='#7f7f7f'))
		figure=go.Figure(data=data,layout=layout)
		comments_chart = opy.plot(figure, auto_open=False, output_type='div')

		context = {
			'comments_chart': comments_chart,
		}
		return render(request, 'event_stats.html', context)
	else:
	    error_message = "Stats are available only\
	          to team members."
	    context = {
	        'error_message': error_message}
	    return render(request, 'CRUDops/error.html', context)
