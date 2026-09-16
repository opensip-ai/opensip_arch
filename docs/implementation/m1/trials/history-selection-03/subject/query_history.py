"""Root02 exact run.show adapter. Identity model and receipt are admitted host inputs.

No provider, current checkout or replacement analysis is consulted. The selected
identity model must be the pinned existing close_run owner, not a caller callback.
"""
import copy

class QueryHistorySourceRefusal(ValueError):
    def __init__(self):super().__init__('REPORT-HISTORY.SOURCE-MISMATCH')

def require(value):
    if not value:raise QueryHistorySourceRefusal()

def unavailable(project_id,run_id,availability):
    require(availability in ('expired','purged','corrupt','unavailable'))
    return {'schemaFamily':'opensip.product.query','schemaMajor':3,'operation':'run.show',
            'context':{'projectId':project_id,'resolvedView':{'runId':run_id},'coverage':'unavailable',
                       'availability':availability,'truncated':False,'totalItems':0,'advisory':False},'items':[]}

def run_show(project_id,run_id,source,identity_model,validate_response):
    """source is one lookup result from the host's retained namespace read snapshot.

    source=unavailable has a closed retained availability reason. A retained source
    contains the exact sealed run, objects, blobs and already admitted terminal
    AnalysisResult receipt. This adapter admits the sealed evidence afresh and
    checks receipt identities and verdict; operational receipt custody/deficiency
    remains a host precondition, not a property inferred from static run bytes.
    """
    require(type(source) is dict)
    if source.get('state')=='unavailable':
        require(set(source)=={'state','availability'})
        out=unavailable(project_id,run_id,source['availability']);validate_response(out);return out
    require(set(source)=={'state','run','objects','blobs','result'} and source['state']=='retained')
    run=source['run'];require(run.get('projectId')==project_id)
    try:
        actual_id=identity_model.close_run(run,source['objects'],source['blobs'])
    except identity_model.EvidenceUnavailable:
        out=unavailable(project_id,run_id,'unavailable');validate_response(out);return out
    except (identity_model.CompleteReplayMismatch,identity_model.C.AdmissionError):
        out=unavailable(project_id,run_id,'corrupt');validate_response(out);return out
    require(actual_id==run_id)
    result=source['result']
    require(result.get('runId')==actual_id and result.get('planId')==run['planId'])
    seal=source['objects'][run['evaluationSealId']]
    require(seal[0]=='evaluation-seal' and result.get('verdict')==seal[1]['verdict'])
    out={'schemaFamily':'opensip.product.query','schemaMajor':3,'operation':'run.show',
         'context':{'projectId':project_id,'resolvedView':{'runId':actual_id},'coverage':'complete',
                    'availability':'retained','truncated':False,'totalItems':1,'advisory':False},
         'items':[{'projectId':project_id,'runId':actual_id,'sealedRun':copy.deepcopy(run),'result':copy.deepcopy(result)}]}
    validate_response(out)
    return out

def admit_response(response,project_id,run_id,validate_response):
    """Consumer joins before using the typed item. Schema shape alone is insufficient."""
    validate_response(response)
    context=response['context'];require(context['projectId']==project_id and context['resolvedView']=={'runId':run_id})
    if context['availability']!='retained':return None
    item=response['items'][0]
    require(item['projectId']==project_id and item['runId']==run_id)
    require(item['sealedRun']['projectId']==project_id and item['result']['runId']==run_id)
    require(item['result']['planId']==item['sealedRun']['planId'])
    return item
