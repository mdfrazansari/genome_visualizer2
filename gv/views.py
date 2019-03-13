from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
import pandas as pd
import os
from django.shortcuts import redirect
from django.utils import timezone
import logging
from .models import Patient
from . import census as cn
from . import genome as gn
from .tasks import create_random_user_accounts
from .forms import PatientForm, gvUserForm
from django.contrib.auth.decorators import login_required


# Create your views here.

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = gvUserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.email = 'mdfraz@iitkgp.ac.in'
            user.is_superuser=False
            user.is_staff=True
            user.save()
            return redirect('/accounts/login')
        else:
            print(form.errors)
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = gvUserForm()
        return render(request, 'registration/register.html', {'form': form})



@login_required
def index(request):
    return redirect("/admin/gv/patient/")
    logger.debug("fraz")
    create_random_user_accounts.delay(8)
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        print(request.FILES)
        
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.creation_date = timezone.now()
            patient.save()
            return redirect('patient_detail', pk=patient.pk)
        else:
            print(form.errors)
    else:
        form = PatientForm()
        return render(request, 'gv/patient_edit.html', {'form': form})


def view_vcf(request, pk):
    create_random_user_accounts.delay(8)
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'gv/cv1new.html', {'patient': patient})


def getPQArmData(request):
    cytobandsfile = os.path.join(os.path.dirname(__file__), 'data/cytobands.csv')
    df = pd.read_csv(cytobandsfile)
    centromere = df[(df.name.str.match(r'p'))][['chrom','chromEnd']].groupby('chrom').tail(1)
    #centromere = centromere[centromere.chrom=='chr17']
    telomere = df[(df.name.str.match(r'q'))][['chrom','chromEnd']].groupby('chrom').tail(1)
    pqArmData = centromere.merge(telomere, on='chrom')
    sorted_key = pqArmData.chrom.apply(lambda x: ('9'+x[3:], x[3:].zfill(2))[x[3:].isdigit()]).sort_values()
    pqArmData = pqArmData.reindex(index=sorted_key.index)
    return HttpResponse(pqArmData.to_json(orient='records'))

def getChromList(request):
    df = pd.DataFrame(['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6',\
                         'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12',\
                         'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18',\
                         'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY'])
    
    return HttpResponse(df.to_json(orient='records'))


def getCytoBand(request, chrom):
    cytobandsfile = os.path.join(os.path.dirname(__file__), 'data/cytobands.csv')
    df = pd.read_csv(cytobandsfile)
    cytoBands = df[(df.chrom == chrom)]
    return HttpResponse(cytoBands.to_json(orient='records'))


def getVariationData(request):
#    d = chromosomes[15:17]
#    k=pd.DataFrame(d)
#    k.index = k.name
#    k.to_json(orient='index')
    return HttpResponse("""{"chr1":{"location":[3607520,3615156,3638674,3643927,3646291,3652617,33986953,34015581,34023749,34033512,34042810,34052403,34052605,34070826,34071525,34158472,34158482,34164286,34189867,34189917,34270187,34270498,34278258,34278562,34279742,34285716,34291056,34291094,34312179,47726087,47748852,47748951,47770987,47776345,47779951,115256669,120466754,120477998,120480394,120491301,120496119,120496127,120508524,120593794,120596847,120612006,120612533,120612762,120614025,120615600,120615627,120621894,120633446,145182056,145182529,145185287,145186368,145186627,145187337,145187838,145187899,145193453,145195645,145196374,145200527,145208623,145208852,145273520,145281247,145285310,185984517,186031363,186086578],"name":"chr1","size":249250621},"chr2":{"location":[10161075,18767384,18772927,29419413,29429888,29444095,29445458,29446202,29497624,29509715,29543663,30143499,30143530,33091978,33141308,33141319,48010628,48010687,48035673,213866714,213886647,213887221,213915104,214012405],"name":"chr2","size":243199373},"chr3":{"location":[47058057,47059323,47103861,119499015,119499507,119499608,119500664,119501039,119501780,119501798,119501960,119530027,119530858,119533910,119535674,119536429,119536581,119536817,119536926,128212526,128212773,136055459,136060139,136471815,155259621,155259656,176738798,176739158,176739663,176745405,176745410,176750426,176764477,176767667,176769608,189455193,189561962,189585852,189590189],"name":"chr3","size":198022430},"chr4":{"location":[1872131,1920894,1954945,1963097,9817070,9817286,106066982,106069030,106160133],"name":"chr4","size":191154276},"chr5":{"location":[23303312,23507631,23507777,23526987,23527239,33438688,35857177,35857207,35861152,35878249,98195818,98196182,98217216,98219090,98225286,110405675,110409067,110412585,110412894,142816908,142819900,142821926,142826792,142827239,142827853,142830915,142837711,142839717,142848579,142848979,142850814,142851247,142851588,142852051,142852928,142856789,142859231,142859419,142859606,142868194,142868277,142895450,142914095,142922087,142923153,142927322,142929053,142934649,142934764,142939231,142944230,142947446,142949541,142951947,142952599,142954168,142956524,142956828,142967308,142967521,142970579,142972345,142972587,142976018,142979183,142982126,142982181,142986673,142991165,142999708,143002263,143002577,143003973,143004258,143005569,143005618,143017939,143019997,143021689,143027696,143034513,143035260,143036439,143048560,143049743,143055846,143059076,143073366,143079929,143082548,143083814,143088452,143095951,143096379,143096901,143096916,143101968,143106090,143107271,143110247,143112062,143112482,143112659,143114552,148205052,148206028,149495050,149499796,149501688,149501751,149504115,149504158,149514958,149515074,149516480,158122679,158134520,158139319,158140222,158446223,158522577,158523584],"name":"chr5","size":180915260},"chr6":{"location":[160448007,160453561,160453978,160465291,160479789,160481537,160483144,160494409,160499736,160517888,160524671,160524773],"name":"chr6","size":171115067},"chr7":{"location":[50348043,50436033,50436948,55086212,55221655,55228053,55229255,55238268,55242609,55266417,55272826,55276010,55276280,55279470,116311519,116311623,116311930,116435768,116438511,140477005,148506396],"name":"chr7","size":159138663},"chr8":{"location":[2792579,2792739,2795835,2796277,2799981,2806920,2820745,2832139,2855892,2901315,2910020,2964684,2966072,2968292,2970477,2970507,2970539,2970627,2971134,2971213,3047166,3142284,3165814,3201012,3201034,3216371,3216383,3224476,3224878,3227107,3257356,3263528,3351259,3351264,3456098,3560090,3566106,3855302,3889764,4494811,15590866,15600787,15622454,15622519,19017935,38287752,38324413,38324421,38324440,38326046,38326161,38326404,81882287,81905287,81905295,82024869,82024954],"name":"chr8","size":146364022},"chr9":{"location":[4984530,4985388,4985542,21968159,21968199,21994713,22009698,36834277,36834414,36834735,36834920,36835488,36836267,36840446,36922960,107262877,139410213,139410424,139411714,139412073,139412197,139418260,139441323],"name":"chr9","size":141213431},"chr10":{"location":[8089033,8089438,8089885,8091030,8091065,8091377,8091423,8092683,8094241,8098185,8105745,8116241,8116598,13369095,61940122,61940128,112326004,112356331],"name":"chr10","size":135534747},"chr11":{"location":[32409549,32410774,32449417,32451920,32452524,32457138,32457675,32457774,32458219,85966542,85966575,85966586,85966665,85968623,85977117,85979010,85980958,108093072,108183167,108203769,118359161,118362414,118393396,119144402,119155649],"name":"chr11","size":135006516},"chr12":{"location":[6697353,6716757,6716759,6716764,11905668,12037318,12045144,25358828,25360138,25361091,25361101,25368462,49439659,92536826,92536839,112924706],"name":"chr12","size":133851895},"chr13":{"location":[28583657,28589662,28602226,28607989,28609825,28610183,28611149,28623938,28636084,28636312,28636446,28645005,28682761,31566014,48878271,48919358,48921884,48947469,48955676],"name":"chr13","size":115169878},"chr14":{"location":[29220010,51324884,51324894,51325057,51325070,51372590,51372606],"name":"chr14","size":107349540},"chr15":{"location":[88403709,88403836,88404391,88405274,88406755,88407221,88407225,88409161,88410449,88410990,88412143,88414005,88414507,88416534,88423463,88429076,88521280,88678680,88679785,99191051,99192483,99416644,99456553,99466969,99467934,99477911,99492045,99501929,99503521,99503800,99506942],"name":"chr15","size":102531392},"chr16":{"location":[3776244,3785675,3795363,3795726,90141477],"name":"chr16","size":90354753},"chr17":{"location":[7572996,7578115,7578645,15942832,15973844,29095920,29482878,29541437,29550141,29653293,29654974,29663624,29670190,29684553,29704002,29705947,37843859,37876835,37883561,37917633,37921194,40451363,40452675],"name":"chr17","size":81195210},"chr18":{"location":[657275,662370,669292,670541,673443],"name":"chr18","size":78077248},"chr19":{"location":[1609267,10464687,10475760,10477067,17935584,17935946],"name":"chr19","size":59128983},"chr20":{"location":[26094564,30959704,31022959],"name":"chr20","size":63025520},"chr21":{"location":[36228360,36228390,36252595,36261761,39739665,40032140,40034216,40034390],"name":"chr21","size":48129895},"chr22":{"location":[22597978,22598808,22599057,22599764,22972464,23521094,23522779,23522810,23540414,23627369,23627441,23632333,23632665,23644631,23644677,23648913,41544167,41545611,41575884],"name":"chr22","size":51304566},"chrX":{"location":[1531648,1546792,1546876,1547070,1572950,44833841,44972968,44977944,48649426,48649449,48649456,53226311,53228148,53254311,53255291,53436232,133507240,133528116,133561242],"name":"chrX","size":155270560},"chrY":{"location":[1267665,1481648,1496792,1496876,1497070],"name":"chrY","size":59373566}}""")


def cv3(request, pk, chrom):
    patient = get_object_or_404(Patient, pk=pk)
    context = {'patient': patient,
               'chrom': chrom}
    return render(request, "gv/cv3.html", context)


@login_required
def cv4(request, pk, chrom):
    patient = get_object_or_404(Patient, pk=pk)
    context = {'patient': patient,
               'chrom': chrom}
    return render(request, "gv/cv4.html", context)


def getPQArmDataChrom(request, chrom):
    cytobandsfile = os.path.join(os.path.dirname(__file__), 'data/cytobands.csv')
    df = pd.read_csv(cytobandsfile)
    centromere = df[(df.name.str.match(r'p'))][['chrom','chromEnd']].groupby('chrom').tail(1)
    centromere = centromere[centromere.chrom==chrom]
    telomere = df[(df.name.str.match(r'q'))][['chrom','chromEnd']].groupby('chrom').tail(1)
    pqArmData = centromere.merge(telomere, on='chrom')
    sorted_key = pqArmData.chrom.apply(lambda x: ('9'+x[3:], x[3:].zfill(2))[x[3:].isdigit()]).sort_values()
    pqArmData = pqArmData.reindex(index=sorted_key.index)
    return HttpResponse(pqArmData.to_json(orient='records'))


def getCensusData(request, chrom):
    census_file = os.path.join(os.path.dirname(__file__), 'data/Census_all.csv')
    c = cn.Census(census_file)
    data = c.getChromosomeCensusData(chrom[3:])
    return HttpResponse(data.to_json(orient='records'))


def getVariationAllDetails(request, pk, chrom):
    patient = Patient.objects.filter(pk=pk).last()
    vcf = gn.VCF(settings.MEDIA_ROOT + "/" +patient.vcf_file.url)
    data = vcf.getVariationAllDetails(chrom)
    return HttpResponse(data.to_json(orient='records'))
    
def getGeneData(request, chrom):
    gene_file = os.path.join(os.path.dirname(__file__), 'data/gene_location.csv')
    df = pd.read_csv(gene_file)
    df = df.sort_values("start")
    return HttpResponse(df[df.chrom == chrom].to_json(orient='records'))
