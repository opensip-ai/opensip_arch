"""Closed presentation receipts; no authentication or source selection is conferred."""
import copy


def closed(properties,required=None,**extra):
    return {'type':'object','additionalProperties':False,'required':list(properties) if required is None else required,'properties':properties,**extra}


def ref(value):return {'$ref':value}


def integrate(report,catalog_schema):
    report=copy.deepcopy(report);defs=report['$defs']
    C='urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/'
    I='urn:opensip:product-v1:identity:v3#/$defs/'
    R='urn:opensip:product-v1:workflows:evaluator3:repair:2#/$defs/'
    K=catalog_schema['$id']+'#/$defs/'
    shapes={
        'capabilities':[copy.deepcopy(catalog_schema['$defs']['CapabilityDescriptionV1']['properties']['capabilityId'])],
        'rules':[copy.deepcopy(catalog_schema['$defs']['RuleDescriptionV1']['properties']['ruleProgramRef']['properties'][k]) for k in ['contributionId','ruleStableId','semanticsMajor','programDigest']],
        'recipes':[copy.deepcopy(catalog_schema['$defs']['RecipeDescriptionV1']['properties']['recipeKey']['properties'][k]) for k in ['contributionId','recipeId','recipeVersion']],
    }
    names={'capabilities':'CapabilityDescriptionV1','rules':'RuleDescriptionV1','recipes':'RecipeDescriptionV1'}
    key_arrays={}
    groups={}
    for group,parts in shapes.items():
        key={'type':'array','prefixItems':parts,'items':False,'minItems':len(parts),'maxItems':len(parts)}
        key_arrays[group]={'type':'array','maxItems':4096,'uniqueItems':True,'items':key,'x-opensip-order':'canonical-set'}
        groups[group]={'type':'array','maxItems':4096,'items':{'oneOf':[
            closed({'state':{'const':'present'},'descriptor':ref(K+names[group])}),
            closed({'state':{'const':'unavailable'},'key':copy.deepcopy(key),'reason':{'const':'descriptor-not-declared'}}),
        ]},'x-opensip-order':'sequence'}
    authority=closed({'registrySha256':ref(C+'Sha256Hex'),'closureId':ref(C+'ClosureId'),'platform':ref(I+'closure/properties/platform')})
    base={'closureId':ref(C+'ClosureId'),'componentManifestDigest':ref(C+'Sha256Hex'),
          'tree':ref(I+'closure/properties/tree'),'platform':ref(I+'closure/properties/platform'),
          'protocolMajor':ref(I+'closure/properties/protocolMajor'),
          'trustOrigin':{'enum':['retained-generation','installed-signed-release','signed-closure-bundle']},
          'capabilityAuthority':{'oneOf':[{'type':'null'},authority]}}
    listing={'allOf':[ref(I+'Blob'),{'properties':{'path':{'const':'.opensip/presentation-catalog.v1.json'}}}]}
    defs['DescriptionReceiptV1']={'oneOf':[
        closed({'state':{'const':'unavailable'},'closureId':ref(C+'ClosureId'),'reason':{'enum':['catalog-not-retained','catalog-corrupt']}}),
        closed({'state':{'const':'no-catalogue-declared'},**copy.deepcopy(base)}),
        closed({'state':{'const':'present'},**copy.deepcopy(base),'listing':listing,**groups}),
    ],'description':'Projection from the catalogue owner after private closure/release/declaration admission. Carries the complete tree, not a new proof of its authentication.'}
    selection=closed({'closureId':ref(C+'ClosureId'),**key_arrays})
    run_selection=copy.deepcopy(selection)
    run_selection['properties']['recipes']['maxItems']=0
    recipe_selection=copy.deepcopy(selection)
    for group in ['capabilities','rules']:recipe_selection['properties'][group]['maxItems']=0
    recipe_selection['properties']['recipes'].update(minItems=1,maxItems=1)
    defs['RunDescriptionsV1']=closed({
        'runId':ref(C+'RunId'),'planId':ref(C+'PlanId'),
        'selection':{'type':'array','maxItems':128,'items':run_selection,'x-opensip-order':{'by':['closureId']}},
        'receipts':{'type':'array','maxItems':128,'items':ref('#/$defs/DescriptionReceiptV1'),'x-opensip-order':'sequence'},
    },description='Capabilities/rules only: recipe selection keys are empty. Closures and keys derive from this exact Run Plan, policy and native release; document indices are not authority.')
    defs['RecipeDescriptionsV1']=closed({'repairPlanId':ref(C+'RepairPlanId'),'recipe':ref(R+'RecipeRef'),
        'selection':recipe_selection,'receipt':ref('#/$defs/DescriptionReceiptV1')},
        description='Exactly the selected preview RecipeRef; capability/rule keys are empty and recipe keys contain exactly this one recipe. Actual evidence source, targets and applicability remain the existing envelope RepairPlanDescriptor.')
    def state(target):return {'oneOf':[closed({'state':{'const':'present'},'data':ref(target)}),ref('#/$defs/PanelNotPresentV1')]}
    provenance={
        'verifiedInDocument':['selection-receipt-order-and-keys','listing-member-of-embedded-tree','capability-association-closure-platform','run-plan-or-preview-recipe-identity-joins','selected-description-keys-in-visible-catalogue','capability-registry-equals-visible-catalogue','at-most-one-visible-capability-authority'],
        'hostAsserted':['authenticated-release-and-closure-association','selected-run-policy-and-declarations','exact-retained-catalogue-bytes','current-trust-admission','omission-byte-delta'],
        'limits':['Embedded selected descriptors do not reconstruct the full catalogue blob','The projected receipt does not reconstruct the complete closure identity preimage','Descriptions cannot change evidence, authority or applicability'],
    }
    defs['DescriptionsPanelV1']=closed({'run':state('#/$defs/RunDescriptionsV1'),'recipe':state('#/$defs/RecipeDescriptionsV1'),'provenance':{'const':provenance}})
    defs['DescriptionsPanelStateV1']=state('#/$defs/DescriptionsPanelV1')
    defs['PanelsV1']['properties']['descriptions']=ref('#/$defs/DescriptionsPanelStateV1')
    priority=defs['BudgetProfileV1']['properties']['projectionPriority']['const'];assert 'descriptions' not in priority;priority.append('descriptions')
    commands=[]
    for condition in report['allOf']:
        command=condition.get('if',{}).get('properties',{}).get('command',{}).get('const')
        if command:
            condition['then']['properties']['panels']['required'].append('descriptions');commands.append(command)
    assert len(commands)==8
    remove={'capability-descriptions','recipe-descriptions','recipe-parameters','rule-descriptions'}
    assert remove<=set(defs['FeatureId']['enum']);defs['FeatureId']['enum']=[v for v in defs['FeatureId']['enum'] if v not in remove]
    for condition in report['allOf']:
        states=condition.get('then',{}).get('properties',{}).get('featureStates',{}).get('const')
        if states is not None:states[:]=[v for v in states if v['featureId'] not in remove]
    return report
