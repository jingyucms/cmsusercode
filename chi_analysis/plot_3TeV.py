from ROOT import *
import ROOT
import array, math
import os

def ratio(g1,g2,addErrors=False):
    if isinstance(g1,TGraph):
        na=g1.GetN()
    else:
        na=g1.GetXaxis().GetNbins()
    if isinstance(g2,TGraph):
        nb=g2.GetN()
    else:
        nb=g2.GetXaxis().GetNbins()
    for a in range(na):
        if isinstance(g1,TGraph):
            x1,y1=(ROOT.Double(),ROOT.Double())
            g1.GetPoint(a,x1,y1)
        else:
            x1=g1.GetBinCenter(a+1)
            y1=g1.GetBinContent(a+1)
        b=a
        if b>=nb+2:
            b=2*nb-a+1
        elif b>=nb:
            b=nb-1
        if isinstance(g2,TGraph):
            x2,y2=(ROOT.Double(),ROOT.Double())
            g2.GetPoint(b,x2,y2)
        else:
            x2=g2.GetBinCenter(b+1)
            y2=g2.GetBinContent(b+1)
        if y2>0:
            factor=1.0/y2
        else:
            factor=0
        if isinstance(g1,TGraph):
            g1.SetPoint(a,x1,y1*factor)
        else:
            g1.SetBinContent(a+1,y1*factor)
            if addErrors:
                g1.SetBinError(a+1,sqrt(pow(g1.GetBinError(a+1)*factor,2)+pow(y1*factor*g2.GetBinError(b+1)*factor,2)))
            else:
                g1.SetBinError(a+1,g1.GetBinError(a+1)*factor)

def make_smooth_graph(h2,h3):
    h2=TGraph(h2)
    h3=TGraph(h3)
    npoints=h3.GetN()
    h3.Set(2*npoints+2)
    for b in range(npoints+2):
        x1,y1=(ROOT.Double(),ROOT.Double())
        if b==0:
            h3.GetPoint(npoints-1,x1,y1)
        elif b==1:
            h2.GetPoint(npoints-b,x1,y1)
        else:
            h2.GetPoint(npoints-b+1,x1,y1)
        h3.SetPoint(npoints+b,x1,y1)
    return h3

def smooth_hist(h1):
    fitmin=3
    fitmax=17
    #print h1.GetXaxis().GetNbins()-fitmin
    if h1.GetXaxis().GetNbins()-fitmin>5:
        f1=TF1("fit","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x+[5]*x*x*x*x*x",fitmin,fitmax)
    elif h1.GetXaxis().GetNbins()-fitmin>4:
        f1=TF1("fit","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x",fitmin,fitmax)
    else:
        f1=TF1("fit","[0]+[1]*x+[2]*x*x",fitmin,fitmax)
#    fitmin=5
#    fitmax=13
#    f1=TF1("fit","[0]+[1]*x+[2]*x*x",fitmin,fitmax)
    h1.Fit(f1,"RQ0")
    for b in range(h1.GetXaxis().GetNbins()):
        if h1.GetBinCenter(b+1)>fitmin+1 and h1.GetBinCenter(b+1)<fitmax-1:
            #print h1.GetBinCenter(b+1),f1.Eval(h1.GetBinCenter(b+1))
            h1.SetBinContent(b+1,f1.Eval(h1.GetBinCenter(b+1)))

def format_hists(hists,colors):
    ymax=0
    for h in hists:
        h.SetTitle("")
        h.SetLineColor(colors[hists.index(h)])
        h.SetMarkerColor(colors[hists.index(h)])
        h.SetFillColor(0)
        h.SetMarkerSize(0)
        h.GetXaxis().SetTitle("#chi_{dijet}") # = exp(|y_{1}-y_{2}|)
        h.GetXaxis().SetTitleFont(42);
        h.GetYaxis().SetTitleFont(42);
        h.GetXaxis().SetRangeUser(1,16)
        h.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        if h.GetMaximum()>ymax: ymax=h.GetMaximum()
    for h in hists:
        h.GetYaxis().SetRangeUser(0,ymax*1.1)
        h.SetMinimum(0)
        h.SetMaximum(ymax*1.1)

def rebin(h1,nbins,binning):
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)*h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)*h1.GetBinWidth(b+1))
    h1=h1.Rebin(nbins,h1.GetName()+"_rebin",binning)
    for b in range(h1.GetXaxis().GetNbins()):
        h1.SetBinContent(b+1,h1.GetBinContent(b+1)/h1.GetBinWidth(b+1))
        h1.SetBinError(b+1,h1.GetBinError(b+1)/h1.GetBinWidth(b+1))
    return h1

def integral(h1):
    integral=0.0
    for b in range(h1.GetXaxis().GetNbins()):
        if h1.GetBinCenter(b+1)>1 and h1.GetBinCenter(b+1)<16:
            integral+=h1.GetBinContent(b+1)*h1.GetBinWidth(b+1)
    return integral

def addAsymmErrors(h1,h2,h3):
    g=TGraphAsymmErrors(h1)
    for b in range(h1.GetXaxis().GetNbins()):
        g.SetPointEYhigh(b,max(0, h2.GetBinContent(b+1)-h1.GetBinContent(b+1),h3.GetBinContent(b+1)-h1.GetBinContent(b+1)))
        g.SetPointEYlow(b,max(0, h1.GetBinContent(b+1)-h2.GetBinContent(b+1),h1.GetBinContent(b+1)-h3.GetBinContent(b+1)))
    return g

if __name__=="__main__":
    gROOT.Reset()
    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(1.2,"Y")
    gStyle.SetPadLeftMargin(0.18)
    gStyle.SetPadBottomMargin(0.11)
    gStyle.SetPadTopMargin(0.03)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetMarkerSize(1.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetStatFontSize(0.020)
    gStyle.SetTitleSize(0.06, "XYZ")
    gStyle.SetLabelSize(0.05, "XYZ")
    gStyle.SetNdivisions(510, "XYZ")
    gStyle.SetLegendBorderSize(0)

    doPaper=False
    doPreliminary=True
    doRatio=False
    weightedBinCenter=False
    alt1=False
    alt2=True
    alt3=True
    alt3a=True
    alt4=False
    addLambda=False
    thicker=False
    doDataData=False
    add2010data=False

    compareNewData=True
    combineNew2011Data=True
    useNewData=False

    run2010new=False
    
    ct10=False

    theories_plot=False
    if theories_plot:
        addLambda=True
    lambdaset=0
    lengths=[6,4,4,4,4,4,4,4]
    lambdasetlength=lengths[lambdaset]
    theories_plot2=False

    prefix="run2012_2_4fb_"

    if theories_plot:
        prefix+="theories"+str(lambdaset)+"_"
    if theories_plot2:
        prefix+="2_"

    if alt4:
        gStyle.SetErrorX(0)

    jetalgo="AK5"
    jettype="PF"

    ### THEORY FILES ###

    mass_bins=[(400,600),
               (600,800),
               (800,1000),
               (1000,1200),
               (1200,1500),
               (1500,1900),
               (1900,2400),
               (2400,3000),
               (3000,7000),
              ] 
    mass_bins2=[0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
               ]
    mass_bins_nlo=[(400,600),
               (600,800),
               (800,1000),
               (1000,1200),
               (1200,1500),
               (1500,1900),
               (1900,2300,2400),
               (2400,2800,3000),
               (3000,3200,4000,5000,7000),
              ] 
    mass_bins_nlo2=[(1,),
                (2,),
                (3,),
                (4,),
                (5,),
                (6,),
                (7,8),
                (9,10),
                (11,12,13,14),
               ]
    NLObins=14
    #mass_bins_nlo=[(400,600),
    #           (600,800),
    #           (800,1000),
    #           (1000,1200),
    #           (1200,1500),
    #           (1500,1900),
    #           (1900,2400),
    #           (2400,3000),
    #           (3000,4000,7000),
    #          ] 
    #mass_bins_nlo2=[(1,),
    #            (2,),
    #            (3,),
    #            (4,),
    #            (5,),
    #            (6,),
    #            (7,),
    #            (8,),
    #            (9,),
    #           ]
    #NLObins=9

    if ct10:
        filename1nu="fnl2622e_ct10_aspdf_nrm.root"
    else:
        filename1nu="fnl2622e_cteq66_aspdf_nrm.root"
    f1_nlo_nunc = TFile.Open(filename1nu)
    
#    filenamec="../fastNLO/fnl2622d-NLO-CONTACT5000.root"
#    f1_contact = TFile.Open(filenamec)
    
    filename_D6T="qcd_D6T_30_50_noHAD_noMPI_fix25_v3-"+jetalgo+"-qcd_D6T_30_50_fix25_v7-"+jetalgo+"-hists.root"
    f_D6T = TFile.Open(filename_D6T)
    
    filename_Z2="qcd_Z2_30_50_noHAD_noMPI_fix25_v3-"+jetalgo+"-qcd_Z2_30_50_fix25_v7-"+jetalgo+"-hists.root"
    f_Z2 = TFile.Open(filename_Z2)
    
    filename_nonpert="nonpert_hists_"+jetalgo+".root"
    f_nonpert = TFile.Open(filename_nonpert)
    
    filename_pdf="fnl2622f-run2011a-NLO-PDF-2_0fb.root"
    f_pdf = TFile.Open(filename_pdf)
    
    new_hists=[]

    chi_bins=[(1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
              (1,2,3,4,5,6,7,8,9,10,12,14,16),
#              (1,2,3,4,5,6,7,8,9,10,12,14,16),
#              (1,2,3,4,5,6,7,8,9,10,12,14,16),
#              (1,3,5,7,10,12,14,16),
              (1,3,5,7,10,12,14,16),
#              (1,5,10,16),
              ]
    chi_binnings=[]
    for mass_bin in chi_bins:
        chi_binnings+=[array.array('d')]
        for chi_bin in mass_bin:
            chi_binnings[-1].append(chi_bin)
    print "chi_bins:",chi_bins

    ### DATA FILES ###

    mass_bins_max=len(chi_bins)

    #if run2010new:
    #    if doRatio:
    #        offsets=[-0.5,0,0.5,1.0,1.5,2.0,2.5,3.5,4.5,7.5]
    #    else:
    #        offsets=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.68]
    #else:
    #    if doRatio:
    #        offsets=[-0.5,-0.5,0,0.5,1.0,1.5,2.0,2.5,3.5,4.5,7.5]
    #    else:
    #        offsets=[0,0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.68]
    if doRatio:
        offsets=[-0.5,0,0.5,1.0,1.5,2.0,3.0,4.0,5.0,7.0]
    else:
        offsets=[0,0.05,0.1,0.15,0.2,0.25,0.35,0.45,0.63]
    if doRatio:
        offsets=[-0.5,0,0.5,1.0,1.5,2.0,2.5,3.2,4.5,7.5]
    else:
        if compareNewData:
            offsets=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.38,0.5,0.73]
        else:
            offsets=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.68]

    if theories_plot:
        if doRatio:
            offsets=[0,0,0,0,0,0,0,0,0,2]
        else:
            offsets=[0,0,0,0,0,0,0,0,0,0.23]

    if jetalgo+jettype=="AK5PF":
        filename_old_data="new2data_hists_norebin_AK5PF.root"
        filename_data="run2011a_2fb_data_hists_AK5PF.root"
        filename_new_2011_data="run2011a_5_0fb_data_hists_AK5PF.root"
        filename_new_data="data_5fb.root"

        # new data
        mjj_jes = [[1.0323192053302788, 0.88484503314023577, 0.73737086095020388, 0.58989668876016088, 0.44242251657011789, 0.29494834438007489, 0.147474172190043, 0.0, 0.14747417219003189, 0.36868543047510194, 0.66363377485518793, 0.95858211923525172], [0.87284629310275808, 0.74815396551665136, 0.62346163793053355, 0.49876931034442684, 0.37407698275832013, 0.24938465517221342, 0.12469232758610671, 0.0, 0.12469232758611781, 0.31173081896527233, 0.56111547413748575, 0.81050012930969917], [0.83700307195109236, 0.71743120452949505, 0.59785933710791994, 0.47828746968634483, 0.35871560226474752, 0.23914373484317242, 0.11957186742157511, 0.0, 0.11957186742158621, 0.29892966855395997, 0.53807340339712129, 0.7772171382402937], [0.88514663300889307, 0.75869711400762263, 0.63224759500635219, 0.50579807600508175, 0.37934855700381132, 0.25289903800254088, 0.12644951900127044, 0.0, 0.12644951900127044, 0.3161237975031761, 0.56902283550571697, 0.82192187350826895], [0.80361162743214365, 0.68880996637041836, 0.57400830530867086, 0.45920664424694557, 0.34440498318519808, 0.22960332212347279, 0.11480166106172529, 0.0, 0.11480166106173639, 0.28700415265433543, 0.51660747477780822, 0.746210796901281], [0.70129234050475553, 0.6011077204326476, 0.50092310036053966, 0.40073848028843173, 0.3005538602163238, 0.20036924014421587, 0.10018462007210793, 0.0, 0.10018462007210793, 0.25046155018026983, 0.4508307903244857, 0.65120003046870156], [1.4118036491669872, 1.2101174135716986, 1.008431177976421, 0.80674494238113237, 0.60505870678585483, 0.40337247119056618, 0.20168623559528864, 0.0, 0.20168623559528864, 0.50421558898821051, 0.90758806017876559, 1.3109605313693429], [0.73523461277310576, 0.63020109666266366, 0.52516758055222157, 0.42013406444177948, 0.31510054833132628, 0.21006703222088419, 0.10503351611044209, 0.0, 0.10503351611044209, 0.26258379027610523, 0.47265082249698942, 0.68271785471787361], [0.58491471464491296, 0.40494095629263205, 0.22496719794035114, 0.0, 0.22496719794036224, 0.40494095629264315, 0.58491471464492406]]
        mjj_jes = [[1.0162185336731189, 0.87104445743410031, 0.72587038119509284, 0.58069630495607427, 0.4355222287170557, 0.29034815247803714, 0.14517407623901857, 0.0, 0.14517407623901857, 0.36293519059753532, 0.65328334307557245, 0.94363149555360959], [0.87781646306821504, 0.75241411120132717, 0.62701175933443931, 0.50160940746755145, 0.37620705560066359, 0.25080470373377572, 0.12540235186688786, 0.0, 0.12540235186688786, 0.31350587966721966, 0.56431058340099538, 0.81511528713478221], [0.82351180790549705, 0.70586726391899113, 0.58822271993250741, 0.47057817594600149, 0.35293363195949556, 0.23528908797298964, 0.11764454398650592, 0.0, 0.11764454398649482, 0.2941113599662537, 0.52940044793924335, 0.76468953591224409], [0.85957643958114449, 0.73677980535526988, 0.61398317112939527, 0.49118653690349845, 0.36838990267762384, 0.24559326845174922, 0.12279663422587461, 0.0, 0.12279663422587461, 0.30699158556469763, 0.55258485401644686, 0.79817812246820719], [0.83518697528168762, 0.71587455024144653, 0.59656212520120544, 0.47724970016096435, 0.35793727512072326, 0.23862485008048218, 0.11931242504024109, 0.0, 0.11931242504024109, 0.29828106260060272, 0.5369059126810849, 0.77553076276156707], [0.59463904979309978, 0.50969061410837124, 0.4247421784236427, 0.33979374273891416, 0.25484530705418562, 0.16989687136945708, 0.08494843568472854, 0.0, 0.084948435684739643, 0.2123710892118158, 0.38226796058127288, 0.55216483195072996], [1.702988260784255, 1.4597042235293456, 1.2164201862744584, 0.97313614901957113, 0.7298521117646839, 0.48656807450977446, 0.24328403725488723, 0.0, 0.24328403725488723, 0.60821009313722918, 1.0947781676470147, 1.5813462421568003], [0.91541863680983937, 0.78464454583699883, 0.65387045486418049, 0.52309636389133995, 0.39232227291849942, 0.26154818194565888, 0.13077409097284054, 0.0, 0.13077409097282944, 0.32693522743209025, 0.58848340937774912, 0.8500315913234191], [0.31410410251379028, 0.21745668635569926, 0.12080927019760823, 0.0, 0.12080927019761933, 0.21745668635571036, 0.31410410251377918]]
        mjj_jer = [[0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353, 0.17213410430000353], [0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622, 0.11642025789999622], [0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434, 0.16017565399999434], [0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515, 0.15424508139999515], [0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937, 0.20566754999999937], [0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043, 0.18539073299999043], [0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917, 0.1007052909999917], [0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235, 0.28868048399999235], [0.59975979099999854, 0.59975979099999854, 0.59975979099999854, 0.59975979099999854, 0.59975979099999854, 0.59975979099999854, 0.59975979099999854]]
        func_offset=20
        mjj_cor = [TF1("f1","0.5*(1.96982627071+-0.0038417714026*x-abs(-9.84901631877e-10)/("+str(func_offset)+"-x))",1,16),TF1("f106","0.5*(1.97951842404+-0.00379695122488*x-abs(-1.13080063399e-10)/("+str(func_offset)+"-x))",1,16),TF1("f214","0.5*(1.97757018658+-0.00161763403703*x-abs(-0.0781017599925)/("+str(func_offset)+"-x))",1,16),TF1("f320","0.5*(1.9743929146+-0.00203846307889*x-abs(-0.0273457974666)/("+str(func_offset)+"-x))",1,16),TF1("f425","0.5*(1.97552078787+-0.0031648924795*x-abs(-0.0276370509323)/("+str(func_offset)+"-x))",1,16),TF1("f530","0.5*(2.00006979085+-0.00229206722881*x-abs(-0.555451658199)/("+str(func_offset)+"-x))",1,16),TF1("f635","0.5*(2.04005424018+0.0011282713032*x-abs(-1.47625047498)/("+str(func_offset)+"-x))",1,16),TF1("f737","0.5*(2.00084153582+-0.00627357155708*x-abs(-0.745379131834)/("+str(func_offset)+"-x))",1,16),TF1("f842","0.5*(2.01172169652+-0.0246255645124*x-abs(0.555605524731)/("+str(func_offset)+"-x))",1,16),]
        mjj_cor_err = [[0.15529128760128294, 0.13349029993888156, 0.11160252571465418, 0.089627445666978278, 0.06756453638321841, 0.045413270258081784, 0.027881209937150833, 0.025862742718938639, 0.021828235507113339, 0.055375204056046817, 0.1007607977581543, 0.14651620367686694], [0.33066468441693436, 0.28047024209325327, 0.23043739688403969, 0.18063337391875675, 0.13114424332485183, 0.082081912030693344, 0.040172892230832632, 0.028884508559641843, 0.073154669672623615, 0.13366807928333102, 0.20807831937386373, 0.26505907909593324], [0.069369893503280933, 0.067704536021465159, 0.076130189834780551, 0.082549820040603364, 0.086539532525345478, 0.087549452136484532, 0.084853175548707596, 0.077470763739775975, 0.070026265065570303, 0.0653841102140158, 0.068324177739517641, 0.28200550112627837], [0.22065955119195674, 0.1838159726204574, 0.1474180634064875, 0.11156760713156573, 0.076394558039657959, 0.042067485888094787, 0.014885583287559883, 0.023589345430016572, 0.053186253960060867, 0.09363785355077929, 0.13294188133106405, 0.13671361998032489], [0.23737652566362261, 0.22310960731535129, 0.20702763859479084, 0.18877784249486801, 0.16790979718454974, 0.14383914163986627, 0.11579379253301297, 0.082731982247351288, 0.063271911456434973, 0.049617117472354741, 0.1861926185054999, 0.46442451864212725], [0.2719331756294241, 0.24944304587742883, 0.22546000422979384, 0.19969504297222551, 0.17177801335807041, 0.141226990094101, 0.1074026219778923, 0.13920813175537222, 0.16195875778909069, 0.16798324237813073, 0.20172462526012458, 0.45800136044463757], [0.46698613940863598, 0.46128510065599915, 0.45036186302212389, 0.43316457806113362, 0.40833543769838598, 0.37409071679197925, 0.3280395755755271, 0.28386005403332121, 0.2574564672424971, 0.16191057548905133, 0.38836590711905494, 1.2308436680453738], [0.8678660228117222, 0.67976817402428369, 0.49651764039941576, 0.31935058052580939, 0.14985644492355438, 0.056748455990554385, 0.15711543332228867, 0.28806340514502554, 0.3974776652041741, 0.50372985898834732, 0.46056048685727841, 0.19229646537497219], [2.7581340119791955, 2.2662330794247278, 1.6825674522324967, 0.75652150171325805, 0.86783003724923291, 2.1476676621752464, 4.9015604239225361]]
        mjj_smear = [[1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009, 1.335034492000009], [1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002, 1.2319856480000002], [0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798, 0.85892269000000798], [1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966, 1.1894261729999966], [1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995, 1.284832178999995], [1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981, 1.3753693309999981], [1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037, 1.7163622570000037], [3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993, 3.074645877999993], [1.9826425900000055, 1.9826425900000055, 1.9826425900000055, 1.9826425900000055, 1.9826425900000055, 1.9826425900000055, 1.9826425900000055]]
        mjj_tails = [[0.45941610295349711, 0.39041575189524003, 0.32141540083633902, 0.2524150497766664, 0.18341469871602789, 0.11441434765416814, 0.045413996590748518, 0.023586354474736115, 0.092586705543007408, 0.19608723215325252, 0.33408793432804229, 0.47208863659283784], [0.11750653713958337, 0.098582711926847866, 0.079658886700850751, 0.060735061458666584, 0.041811236196398482, 0.022887410908800643, 0.003963585588651064, 0.014960239774342021, 0.033884065195288748, 0.062269803489722886, 0.10011745512711334, 0.13796510863658407], [0.15718323580524718, 0.1385619040630337, 0.11985882270943438, 0.10105582516414802, 0.082128931541158856, 0.063045821124557699, 0.043761860544733189, 0.024213623434343745, 0.0043078357237991138, 0.026556456904991421, 0.071275414313343166, 0.12754325610701001], [0.14727026705739776, 0.13794629209908926, 0.12776817500165238, 0.11654610640083884, 0.10402953793582359, 0.089880773989864382, 0.073633472996981197, 0.054624939047615007, 0.031880619333601867, 0.012742757700490159, 0.10950505674833799, 0.32693323599439772], [0.27850335868829235, 0.25267341900053752, 0.22599155275447314, 0.19826844293713286, 0.16925419109142248, 0.13861197755775656, 0.10587667042529225, 0.070387292768109289, 0.031171819695102743, 0.038131033271360248, 0.16770263899936744, 0.41762712665807111], [0.90876155213568399, 0.85579865932572941, 0.79803371556963487, 0.73439959843493163, 0.66348770631074472, 0.5833994891998151, 0.49151313996308454, 0.38410293266608608, 0.25568985858166471, 0.0039996846153966814, 0.54109081021083139, 1.7645739022708495], [1.8622834437571512, 1.8097421113915935, 1.746367813075228, 1.6697532230412093, 1.576720671277293, 1.4629872112452535, 1.3226382977256257, 1.1472690506697025, 0.92451935235877136, 0.45713728573771317, 0.63865880435896027, 3.2648434699919959], [1.7977399235878544, 1.6624334518192729, 1.521534622713927, 1.373800690196969, 1.2175912294496161, 1.0506952331074071, 0.87005940528611658, 0.67134485183443782, 0.44817084605930368, 0.044617627736875942, 0.73743636695285941, 2.3095306716903075], [4.2158319865265801, 3.3168919064300528, 2.3759791185036629, 1.1004290887354329, 0.39602992961106365, 1.9749278765515355, 4.6283271439367617]]

    f_data = TFile.Open(filename_data)
    f_old_data = TFile.Open(filename_old_data)
    f_new_2011_data = TFile.Open(filename_new_2011_data)
    f_new_data = TFile.Open(filename_new_data)

    ### THEORY AND DATA PLOT ###
    
    new_hists=[]
    data_hists=[]
    data_hists2=[]
    unsmeared_data_events=[]

    table={}
    table["Mjj"]=[]
    table["chi"]=[]
    table["chi_low"]=[]
    table["chi_high"]=[]
    table["chi_center"]=[]
    table["N_raw"]=[]
    table["c_unsmear"]=[]
    table["N_unsmeared"]=[]
    table["N_normalized"]=[]
    table["N_qcd_normalized"]=[]
    table["N_qcdci_normalized"]=[]
    table["Stat"]=[]
    table["JES"]=[]
    table["JER"]=[]
    table["JERtails"]=[]
    table["Unsmear"]=[]
    table["SIM"]=[]
    table["Scale+"]=[]
    table["Scale-"]=[]
    table["PDF+"]=[]
    table["PDF-"]=[]
    table["NPC+"]=[]
    table["NPC-"]=[]
    table["TotalTheory+"]=[]
    table["TotalTheory-"]=[]
    table["TotalData"]=[]
    table["Total"]=[]

    #c = TCanvas("nlo-final", "nlo-final", 0, 0, 400, 500)
    c = TCanvas("nlo-final", "nlo-final", 0, 0, 400, 600)
    if theories_plot:
        c = TCanvas("nlo-final", "nlo-final", 0, 0, 300, 300)
    c.Divide(1,1)
    first=True
    if run2010new:
         rang=reversed(range(1,mass_bins_max+1))
    else:
         #rang=reversed(range(2,mass_bins_max+2))
         rang=reversed(range(1,mass_bins_max+1))
    if theories_plot:
         rang=reversed(range(mass_bins_max,mass_bins_max+1))
    if theories_plot2:
         rang=reversed(range(mass_bins_max-1,mass_bins_max))
    for mx in rang:
        #if not run2010new and mx<=2:
        #    continue
        mold=mx
        if mx>=9:
           mold=9
        #if run2010new:
        if True:
            m=mx
        #else:
        #    m=mx-1
        
        print "mass bin: ",mx,"(2011)",mold,"(2010SYS)",m,"(2010NLO)"

        ### NON-PERTUBATIVE-CORRECTIONS ###

        histname="DiJet_NPcor_MBin"
        histname+=str(mx-1)+""
        non_pert_corr = TH1F(f_nonpert.Get(histname))
        non_pert_corr=rebin(non_pert_corr,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])

        histname="DiJet_NPcor_up_MBin"
        histname+=str(mx-1)+""
        h2np = TH1F(f_nonpert.Get(histname))
        h2np=rebin(h2np,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])

        histname="DiJet_NPcor_down_MBin"
        histname+=str(mx-1)+""
        h3np = TH1F(f_nonpert.Get(histname))
        h3np=rebin(h3np,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])

        ### NLO ###

        first1=True
        for i in range(len(mass_bins_nlo[mx-1])-1):
            histname="h30"
            if mass_bins_nlo2[mx-1][i]<10: histname+="0"
            histname+=str(mass_bins_nlo2[mx-1][i])+"00"
            h1 = TH1F(f1_nlo_nunc.Get(histname))
            h1.Scale(float(mass_bins_nlo[mx-1][i+1]-mass_bins_nlo[mx-1][i]))
            h1=rebin(h1,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            histname="h30"
            if mass_bins_nlo2[mx-1][i]+NLObins<10: histname+="0"
            histname+=str(mass_bins_nlo2[mx-1][i]+NLObins)+"08"
            h2 = TH1F(f1_nlo_nunc.Get(histname))
            h2=rebin(h2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            histname="h30"
            if mass_bins_nlo2[mx-1][i]+NLObins<10: histname+="0"
            histname+=str(mass_bins_nlo2[mx-1][i]+NLObins)+"09"
            h3 = TH1F(f1_nlo_nunc.Get(histname))
            h3=rebin(h3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            h2.Scale(integral(h1))
            h3.Scale(integral(h1))
            if not ct10:
                histname="h30"
                if mass_bins_nlo2[mx-1][i]+NLObins<10: histname+="0"
                histname+=str(mass_bins_nlo2[mx-1][i]+NLObins)+"01"
                h2p = TH1F(f1_nlo_nunc.Get(histname))
                h2p=rebin(h2p,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
                histname="h30"
                if mass_bins_nlo2[mx-1][i]+NLObins<10: histname+="0"
                histname+=str(mass_bins_nlo2[mx-1][i]+NLObins)+"02"
                h3p = TH1F(f1_nlo_nunc.Get(histname))
                h3p=rebin(h3p,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
                h2p.Scale(integral(h1))
                h3p.Scale(integral(h1))
            if first1==True:
                new_hists+=[h1]
                new_hists+=[h2]
                new_hists+=[h3]
                if not ct10:
                    new_hists+=[h2p]
                    new_hists+=[h3p]
                first1=False
            else:
                if not ct10:
                    new_hists[-1].Add(h3p)
                    h3p=new_hists[-1]
                    new_hists[-2].Add(h2p)
                    h2p=new_hists[-2]
                    new_hists[-3].Add(h3)
                    h3=new_hists[-3]
                    new_hists[-4].Add(h2)
                    h2=new_hists[-4]
                    new_hists[-5].Add(h1)
                    h1=new_hists[-5]
                else:
                    new_hists[-1].Add(h3)
                    h3=new_hists[-1]
                    new_hists[-2].Add(h2)
                    h2=new_hists[-2]
                    new_hists[-3].Add(h1)
                    h1=new_hists[-3]
        h2.Scale(1./integral(h1))
        h3.Scale(1./integral(h1))
        if not ct10:
            h2p.Scale(1./integral(h1))
            h3p.Scale(1./integral(h1))

        h1.Multiply(non_pert_corr)
        smooth_hist(h1)

        h1_alt=TH1F(h1)
        new_hists+=[h1_alt]

        h1_alt2=[]
        for i in range(lambdasetlength):
            h1_alt2+=[TH1F(h1)]
            new_hists+=[h1_alt2]

        h1.Scale(1./integral(h1))

        h2.Multiply(h1)
        h2.Add(h1)
        #h2.Multiply(non_pert_corr)
        #h2.Scale(1./integral(h2))

        h3.Multiply(h1)
        h3.Add(h1)
        #h3.Multiply(non_pert_corr)
        #h3.Scale(1./integral(h3))

        format_hists([h1,h2,h3],[1,2,2])

        ### PDF ERRORS ###
        
        if ct10:
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])+"down"
            h2p = TH1F(f_pdf.Get(histname))
            h2p=rebin(h2p,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])

            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])+"up"
            h3p = TH1F(f_pdf.Get(histname))
            h3p=rebin(h3p,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            for b in range(h3p.GetXaxis().GetNbins()):
                print h2p.GetBinContent(b+1),h3p.GetBinContent(b+1)

        h2p.Multiply(h1)
        h2p.Add(h1)
        #h2p.Multiply(non_pert_corr)
        #h2p.Scale(1./integral(h2p))

        h3p.Multiply(h1)
        h3p.Add(h1)
        #h3p.Multiply(non_pert_corr)
        #h3p.Scale(1./integral(h3p))

        ### NLO ERROR BAND ###

        h3a=TGraphAsymmErrors()
        for b in range(h1.GetXaxis().GetNbins()):
            b2s=h2.GetBinContent(b+1)
            b3s=h3.GetBinContent(b+1)
            b2p=h2p.GetBinContent(b+1)
            b3p=h3p.GetBinContent(b+1)
            b2np=h2np.GetBinContent(b+1)
            b3np=h3np.GetBinContent(b+1)
            # scale
            #h2.SetBinContent(b+1,h1.GetBinContent(b+1)-(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2s,b3s)))
            #h3.SetBinContent(b+1,h1.GetBinContent(b+1)+(max(h1.GetBinContent(b+1),b2s,b3s)-h1.GetBinContent(b+1)))
            # PDF
            #h2.SetBinContent(b+1,h1.GetBinContent(b+1)-(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2p,b3p)))
            #h3.SetBinContent(b+1,h1.GetBinContent(b+1)+(max(h1.GetBinContent(b+1),b2p,b3p)-h1.GetBinContent(b+1)))
            # np
            #h2.SetBinContent(b+1,h1.GetBinContent(b+1)-(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1))))
            #h3.SetBinContent(b+1,h1.GetBinContent(b+1)+(max(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1))-h1.GetBinContent(b+1))-h1.GetBinContent(b+1))
            # scale+PDF
            #h2.SetBinContent(b+1,h1.GetBinContent(b+1)-sqrt(pow(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2s,b3s),2)+
            #                                                pow(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2p,b3p),2)))
            #h3.SetBinContent(b+1,h1.GetBinContent(b+1)+sqrt(pow(max(h1.GetBinContent(b+1),b2s,b3s)-h1.GetBinContent(b+1),2)+
            #                                                pow(max(h1.GetBinContent(b+1),b2p,b3p)-h1.GetBinContent(b+1),2)))
            # scale+PDF+np
            up=sqrt(pow(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2s,b3s),2)+
                    pow(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2p,b3p),2)+
                    pow(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1)),2))
            down=sqrt(pow(max(h1.GetBinContent(b+1),b2s,b3s)-h1.GetBinContent(b+1),2)+
                      pow(max(h1.GetBinContent(b+1),b2p,b3p)-h1.GetBinContent(b+1),2)+
                      pow(max(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1))-h1.GetBinContent(b+1),2))
            h2.SetBinContent(b+1,h1.GetBinContent(b+1)-up)
            h3.SetBinContent(b+1,h1.GetBinContent(b+1)+down)
            print h1.GetBinContent(b+1),\
            "-scale",h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2s,b3s),\
            "+scale",max(h1.GetBinContent(b+1),b2s,b3s)-h1.GetBinContent(b+1),\
            "-pdf",h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2p,b3p),\
            "+pdf",max(h1.GetBinContent(b+1),b2p,b3p)-h1.GetBinContent(b+1),\
            "-np",h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1)),\
            "+np",max(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1))-h1.GetBinContent(b+1)

            table["N_qcd_normalized"]+=[h1.GetBinContent(b+1)]
            table["Scale-"]+=[(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2s,b3s))/h1.GetBinContent(b+1)]
            table["Scale+"]+=[(max(h1.GetBinContent(b+1),b2s,b3s)-h1.GetBinContent(b+1))/h1.GetBinContent(b+1)]
            table["PDF-"]+=[(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),b2p,b3p))/h1.GetBinContent(b+1)]
            table["PDF+"]+=[(max(h1.GetBinContent(b+1),b2p,b3p)-h1.GetBinContent(b+1))/h1.GetBinContent(b+1)]
            table["NPC-"]+=[(h1.GetBinContent(b+1)-min(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1)))/h1.GetBinContent(b+1)]
            table["NPC+"]+=[(max(h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b2np+h1.GetBinContent(b+1),h1.GetBinContent(b+1)*b3np+h1.GetBinContent(b+1))-h1.GetBinContent(b+1))/h1.GetBinContent(b+1)]
            table["TotalTheory-"]+=[(h1.GetBinContent(b+1)-h2.GetBinContent(b+1))/h1.GetBinContent(b+1)]
            table["TotalTheory+"]+=[(h3.GetBinContent(b+1)-h1.GetBinContent(b+1))/h1.GetBinContent(b+1)]

        #smooth_hist(h2)
        #smooth_hist(h3)
        if not alt3:
            h3=make_smooth_graph(h2,h3)
        new_hists+=[h3]

        ### CONTACT ###

        if mx>100:
 
         if lambdaset==0:
            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-7000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            h1_alt.Add(hc2,1)
            #smooth_hist(h1_alt)
            h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Lambda-7000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            h1_alt2[0].Add(hc3,1)
            smooth_hist(h1_alt2[0])
            h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[4]=hc3
            #h1_alt2[4].Scale(1./integral(h1_alt2[4]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            smooth_hist(hc3)
            h1_alt2[5]=hc3
            h1_alt2[5].Scale(1./integral(h1_alt2[5]))

         if lambdaset==1:
            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-5000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc2.SetName(histname+"0")
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt.Add(hc2,1)
            h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-6000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"1")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0].Add(hc3,1)
            h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-7000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"2")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1].Add(hc3,1)
            h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-8000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"3")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2].Add(hc3,1)
            h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_DILHC_2011_Lambda-9000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"4")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3].Add(hc3,1)
            h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==2:
            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Lambda-6000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc2.SetName(histname+"0")
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt.Add(hc2,1)
            h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Lambda-7000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"1")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0].Add(hc3,1)
            h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Lambda-8000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"2")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1].Add(hc3,1)
            h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Add_Lambda-10000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"3")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2].Add(hc3,1)
            h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/cidijet_DijetChi_CILHC_2011_Add_Lambda-12000_Order-1.root"
            histname="chi-"+str(mass_bins[mx-1][0])+"-"+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            hc3.SetName(histname+"4")
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3].Add(hc3,1)
            h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==3:
            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT5000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            #hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt=hc2
            #h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT6000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0]=hc3
            #h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            #h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT8000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT9000Lambda+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==4:
            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            #hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt=hc2
            #h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT9000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0]=hc3
            #h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT11000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            #h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT13000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT15000Lambda-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==5:
            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            #hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt=hc2
            #h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT8000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0]=hc3
            #h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT9000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            #h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT10000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT11000LambdaVV+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==6:
            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            #hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt=hc2
            #h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT9000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0]=hc3
            #h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT11000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            #h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT13000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT15000LambdaVV-LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))

         if lambdaset==7:
            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT5000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc2 = TFile.Open(filename).Get(histname)
            #hc2=rebin(hc2,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc2]
            #smooth_hist(hc2)
            h1_alt=hc2
            #h1_alt.Scale(1./integral(h1_alt))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT6000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[0]=hc3
            #h1_alt2[0].Scale(1./integral(h1_alt2[0]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT7000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[1]=hc3
            #h1_alt2[1].Scale(1./integral(h1_alt2[1]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT8000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[2]=hc3
            #h1_alt2[2].Scale(1./integral(h1_alt2[2]))

            filename="../fastNLO/klaus2011jul/fnl2622e-run2011a-NLO-CONTACT9000LambdaVA+LO_2_0fb.root"
            histname="chi "+str(mass_bins[mx-1][0])+" "+str(mass_bins[mx-1][1])
            hc3 = TFile.Open(filename).Get(histname)
            #hc3=rebin(hc3,len(chi_binnings[mx-1])-1,chi_binnings[mx-1])
            new_hists+=[hc3]
            #smooth_hist(hc3)
            h1_alt2[3]=hc3
            #h1_alt2[3].Scale(1./integral(h1_alt2[3]))


        for b in range(h1_alt.GetXaxis().GetNbins()):
            table["N_qcdci_normalized"]+=[h1_alt.GetBinContent(b+1)]

        ### DATA ###

        print " Mass bin ", mx
        if True:
            histname="DiJet_MBin"
            #if m==1: histname="DiJet_MBin" #1
            #if m==2: histname="DiJet_MBin" #1
            #if m==3: histname="DiJet_MBin"
            #if m==4: histname="DiJet_MBin"
            #if m==5: histname="DiJet_MBin" #2
            #if m==6: histname="DiJet_MBin" #2
            histname+=str(mx-1)+""
            h0 = TH1F(f_data.Get(histname))
            if add2010data and not doDataData and not run2010new:
              if mx<10:
                h0old = TH1F(f_old_data.Get(histname))
                h0.Add(h0old)
            if combineNew2011Data:
                h0new = TH1F(f_new_2011_data.Get(histname))
                h0.Add(h0new)
            if useNewData:
                h0 = TH1F(f_new_data.Get(histname))

            #weighted_bin_centers=[]
            #for i in range(len(chi_binnings[m-1])-1):
            #    weighted_bin_center=0
            #    sum_bin_content=0
            #    for b in range(h0.GetXaxis().GetNbins()):
            #        if h0.GetBinCenter(b+1)>chi_binnings[m-1][i] and h0.GetBinCenter(b+1)<chi_binnings[m-1][i+1]:
            #            weighted_bin_center+=h0.GetBinCenter(b+1)*h0.GetBinContent(b+1)
            #            sum_bin_content+=h0.GetBinContent(b+1)
            #    weighted_bin_centers+=[weighted_bin_center/sum_bin_content]
            h0=rebin(h0,len(chi_binnings[m-1])-1,chi_binnings[m-1])

            print integral(h0)
            data_hists2+=[TH1F(h0)]
            corrections=[]
            for b in range(h0.GetXaxis().GetNbins()):
                # for Suvadeeps input
                #h0.SetBinContent(b+1,h0.GetBinContent(b+1)/h0.GetBinWidth(b+1))
                #h0.SetBinError(b+1,h0.GetBinError(b+1)/h0.GetBinWidth(b+1))
                # end for Suvadeeps input
                #table["chi_center"]+=[weighted_bin_centers[b]]
                table["N_raw"]+=[h0.GetBinContent(b+1)*h0.GetBinWidth(b+1)]
                corrections+=[h0.GetBinContent(b+1)/integral(h0)]
                table["c_unsmear"]+=[mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1))]
                h0.SetBinContent(b+1,h0.GetBinContent(b+1)*mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1)))
                #table["c_unsmear"]+=[mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1))*mjj_smear_cor[mold-1].Eval(h0.GetBinCenter(b+1))]
                #h0.SetBinContent(b+1,h0.GetBinContent(b+1)*mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1))*mjj_smear_cor[mold-1].Eval(h0.GetBinCenter(b+1)))
                table["N_unsmeared"]+=[h0.GetBinContent(b+1)*h0.GetBinWidth(b+1)]
            n=integral(h0)
            unsmeared_data_events+=[n]
            for b in range(h0.GetXaxis().GetNbins()):
                #n_i=h0.GetBinContent(b+1)*h0.GetBinWidth(b+1)
                #p_i=n_i/n
                # Poisson correct
                h0.SetBinError(b+1,h0.GetBinError(b+1)*mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1)))
                #h0.SetBinError(b+1,h0.GetBinError(b+1)*mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1))*mjj_smear_cor[mold-1].Eval(h0.GetBinCenter(b+1)))
                # Poisson modified
                #h0.SetBinError(b+1,h0.GetBinError(b+1)*sqrt(mjj_cor[mold-1].Eval(h0.GetBinCenter(b+1))))
                # Poisson modified
                #h0.SetBinError(b+1,sqrt(n_i)/h0.GetBinWidth(b+1))
                # Multinominal modified
                #h0.SetBinError(b+1,sqrt(n*p_i*(1-p_i))/h0.GetBinWidth(b+1))
                if h0.GetBinContent(b+1)>0:
                    table["Stat"]+=[h0.GetBinError(b+1)/h0.GetBinContent(b+1)]
                else:
                    table["Stat"]+=[0]
              
            if integral(h0)>0:
                data_hists2[-1].Scale(1./integral(h0))
                h0.Scale(1./integral(h0))
            for b in range(h0.GetXaxis().GetNbins()):
                corrections[b]=h0.GetBinContent(b+1)/corrections[b]
            print "corrections", corrections
            h0.SetMarkerStyle(20) #24
            if thicker:
                h0.SetMarkerSize(1.2)
            else:
                h0.SetMarkerSize(0.7)
            new_hists+=[h0]
            data_hists+=[TH1F(h0)]
            h0all=TH1F(h0)
            h0all.SetMarkerStyle(0)
            h0all.SetMarkerSize(0)
            h0sys=TH1F(h0)
            #h0sys.SetMarkerStyle(0)
            #h0sys.SetMarkerSize(0)
            for b in range(h0.GetXaxis().GetNbins()):
                #err_usm_tot0 = sqrt(pow((mjj_cor_err[mold-1][b]/100)*h0.GetBinContent(b+1),2))
                err_usm_tot0 = sqrt(pow((mjj_smear[mold-1][b]/100)*h0.GetBinContent(b+1),2)+
                                pow((mjj_cor_err[mold-1][b]/100)*h0.GetBinContent(b+1),2))
                #err_usm_tot0 = sqrt(pow((mjj_smear_cor_err[mold-1][b]/100)*h0.GetBinContent(b+1),2)+
                #                pow((mjj_cor_err[mold-1][b]/100)*h0.GetBinContent(b+1),2))
                err_sys_tot0 = sqrt(pow(err_usm_tot0,2)+
                                pow((mjj_tails[mold-1][b]/100)*h0.GetBinContent(b+1),2)+
                                pow((mjj_jer[mold-1][b]/100)*h0.GetBinContent(b+1),2)+
                                pow((mjj_jes[mold-1][b]/100)*h0.GetBinContent(b+1),2))
                err_tot0 = sqrt(pow(h0.GetBinError(b+1),2)+pow(err_sys_tot0,2))
                #print "Value: ", round(h0.GetBinContent(b+1),4), " stat:",round(h0.GetBinError(b+1),4),"smear:",round((mjj_smear[mold-1]/100)*h0.GetBinContent(b+1),4),"jer:",round((mjj_jer[mold-1][b]/100)*h0.GetBinContent(b+1),4),"jes:",round((mjj_jes[mold-1][b]/100)*h0.GetBinContent(b+1),4),"cor:",round((mjj_cor_err[mold-1][b]/100)*h0.GetBinContent(b+1),4),"total:",round(err_tot0,4) #,"jeseta:",round((mjj_etajes[m-1][b]/100)*h0.GetBinContent(b+1),4)

                h0sys.SetBinContent(b+1,h0.GetBinContent(b+1))
                h0sys.SetBinError(b+1,err_sys_tot0)
                h0all.SetBinContent(b+1,h0.GetBinContent(b+1))
                h0all.SetBinError(b+1,err_tot0)

                table["JES"]+=[mjj_jes[mold-1][b]/100]
                table["JER"]+=[mjj_jer[mold-1][b]/100]
                table["JERtails"]+=[mjj_tails[mold-1][b]/100]
                if h0.GetBinContent(b+1)>0:
                    table["Unsmear"]+=[(mjj_cor_err[mold-1][b]/100)]
                    table["SIM"]+=[(mjj_smear[mold-1][b]/100)]
                    table["TotalData"]+=[err_sys_tot0/h0.GetBinContent(b+1)]
                else:
                    table["Unsmear"]+=[0]
                    table["TotalData"]+=[0]
                if m==mass_bins_max:
                    table["Mjj"]+=[str(mass_bins[m-1][0])+"-$\infty$"]
                else:
                    table["Mjj"]+=[str(mass_bins[m-1][0])+"-"+str(mass_bins[m-1][1])]
                table["chi"]+=[str(chi_bins[m-1][b])+"-"+str(chi_bins[m-1][b+1])]
                table["chi_low"]+=[str(chi_bins[m-1][b])]
                table["chi_high"]+=[str(chi_bins[m-1][b+1])]
                table["N_normalized"]+=[h0.GetBinContent(b+1)]

            new_hists+=[h0all]
            new_hists+=[h0sys]
        
        ### OLD DATA ###

        print " Mass bin ", mx
        if mx<10:
            histname="DiJet_MBin"
            histname+=str(mx-1)+""
            h0old = TH1F(f_old_data.Get(histname))
            h0old.SetLineColor(2)
            h0old.SetMarkerColor(2)

            #weighted_bin_centers=[]
            #for i in range(len(chi_binnings[m-1])-1):
            #    weighted_bin_center=0
            #    sum_bin_content=0
            #    for b in range(h0old.GetXaxis().GetNbins()):
            #        if h0old.GetBinCenter(b+1)>chi_binnings[m-1][i] and h0old.GetBinCenter(b+1)<chi_binnings[m-1][i+1]:
            #            weighted_bin_center+=h0old.GetBinCenter(b+1)*h0old.GetBinContent(b+1)
            #            sum_bin_content+=h0old.GetBinContent(b+1)
            #    weighted_bin_centers+=[weighted_bin_center/sum_bin_content]
            h0old=rebin(h0old,len(chi_binnings[m-1])-1,chi_binnings[m-1])

            for b in range(h0old.GetXaxis().GetNbins()):
                # for Suvadeeps input
                #h0old.SetBinContent(b+1,h0old.GetBinContent(b+1)/h0old.GetBinWidth(b+1))
                #h0old.SetBinError(b+1,h0old.GetBinError(b+1)/h0old.GetBinWidth(b+1))
                # end for Suvadeeps input
                #table["chi_center"]+=[weighted_bin_centers[b]]
                h0old.SetBinContent(b+1,h0old.GetBinContent(b+1)*mjj_cor[mold-1].Eval(h0old.GetBinCenter(b+1)))
            n=integral(h0old)
            unsmeared_data_events+=[n]
            for b in range(h0old.GetXaxis().GetNbins()):
                #n_i=h0old.GetBinContent(b+1)*h0old.GetBinWidth(b+1)
                #p_i=n_i/n
                # Poisson correct
                h0old.SetBinError(b+1,h0old.GetBinError(b+1)*mjj_cor[mold-1].Eval(h0old.GetBinCenter(b+1)))
                # Poisson modified
                #h0old.SetBinError(b+1,h0old.GetBinError(b+1)*sqrt(mjj_cor[mold-1].Eval(h0old.GetBinCenter(b+1))))
                # Poisson modified
                #h0old.SetBinError(b+1,sqrt(n_i)/h0old.GetBinWidth(b+1))
                # Multinominal modified
                #h0old.SetBinError(b+1,sqrt(n*p_i*(1-p_i))/h0old.GetBinWidth(b+1))
                
            if integral(h0old)>0:
                h0old.Scale(1./integral(h0old))
            h0old.SetMarkerStyle(20) #24
            if thicker:
                h0old.SetMarkerSize(1.2)
            else:
                h0old.SetMarkerSize(0.7)
            new_hists+=[h0old]
            #data_hists+=[TH1F(h0old)]
            h0oldall=TH1F(h0old)
            h0oldall.SetMarkerStyle(0)
            h0oldall.SetMarkerSize(0)
            h0oldsys=TH1F(h0old)
            h0oldsys.SetMarkerStyle(0)
            h0oldsys.SetMarkerSize(0)
            for b in range(h0old.GetXaxis().GetNbins()):
                #err_usm_tot0 = sqrt(pow((mjj_cor_err[mold-1][b]/100)*h0old.GetBinContent(b+1),2))
                err_usm_tot0 = sqrt(pow((mjj_smear[mold-1][b]/100)*h0old.GetBinContent(b+1),2)+
                                pow((mjj_cor_err[mold-1][b]/100)*h0old.GetBinContent(b+1),2))
                err_sys_tot0 = sqrt(pow(err_usm_tot0,2)+
                                pow((mjj_tails[mold-1][b]/100)*h0old.GetBinContent(b+1),2)+
                                pow((mjj_jer[mold-1][b]/100)*h0old.GetBinContent(b+1),2)+
                                pow((mjj_jes[mold-1][b]/100)*h0old.GetBinContent(b+1),2))
                err_tot0 = sqrt(pow(h0old.GetBinError(b+1),2)+pow(err_sys_tot0,2))
                #print "Value: ", round(h0old.GetBinContent(b+1),4), " stat:",round(h0old.GetBinError(b+1),4),"smear:",round((mjj_smear[mold-1]/100)*h0old.GetBinContent(b+1),4),"jer:",round((mjj_jer[mold-1][b]/100)*h0old.GetBinContent(b+1),4),"jes:",round((mjj_jes[mold-1][b]/100)*h0old.GetBinContent(b+1),4),"cor:",round((mjj_cor_err[mold-1][b]/100)*h0old.GetBinContent(b+1),4),"total:",round(err_tot0,4) #,"jeseta:",round((mjj_etajes[m-1][b]/100)*h0old.GetBinContent(b+1),4)

                h0oldsys.SetBinContent(b+1,h0old.GetBinContent(b+1))
                h0oldsys.SetBinError(b+1,err_sys_tot0)
                h0oldall.SetBinContent(b+1,h0old.GetBinContent(b+1))
                h0oldall.SetBinError(b+1,err_tot0)

            new_hists+=[h0oldall]
            new_hists+=[h0oldsys]
        
        ### NEW DATA ###

        if compareNewData:
            #histname="DiJet_MBin"
            #histname+=str(mx-1)+""
            histname="dijet_"+str(mass_bins[mx-1][0])+"_"+str(mass_bins[mx-1][1])+"_chi"
            h0new = TH1F(f_new_data.Get(histname))
            h0new=rebin(h0new,len(chi_binnings[m-1])-1,chi_binnings[m-1])
            for b in range(h0new.GetXaxis().GetNbins()):
                h0new.SetBinContent(b+1,h0new.GetBinContent(b+1)*mjj_cor[mold-1].Eval(h0new.GetBinCenter(b+1)))
                h0new.SetBinError(b+1,h0new.GetBinError(b+1)*mjj_cor[mold-1].Eval(h0new.GetBinCenter(b+1)))
            if integral(h0new)>0:
                h0new.Scale(1./integral(h0new))
            h0new.SetMarkerStyle(21) #24
            if thicker:
                h0new.SetMarkerSize(1.2)
            else:
                h0new.SetMarkerSize(0.7)
            new_hists+=[h0new]
            data_hists+=[TH1F(h0new)]
            h0newall=TH1F(h0new)
            h0newall.SetMarkerStyle(0)
            h0newall.SetMarkerSize(0)
            h0newsys=TH1F(h0new)
            for b in range(h0new.GetXaxis().GetNbins()):
                #err_usm_tot0 = sqrt(pow((mjj_cor_err[mold-1][b]/100)*h0new.GetBinContent(b+1),2))
                err_usm_tot0 = sqrt(pow((mjj_smear[mold-1][b]/100)*h0new.GetBinContent(b+1),2)+
                                pow((mjj_cor_err[mold-1][b]/100)*h0new.GetBinContent(b+1),2))
                #err_usm_tot0 = sqrt(pow((mjj_smear_cor_err[mold-1][b]/100)*h0new.GetBinContent(b+1),2)+
                #                pow((mjj_cor_err[mold-1][b]/100)*h0new.GetBinContent(b+1),2))
                err_sys_tot0 = sqrt(pow(err_usm_tot0,2)+
                                pow((mjj_tails[mold-1][b]/100)*h0new.GetBinContent(b+1),2)+
                                pow((mjj_jer[mold-1][b]/100)*h0new.GetBinContent(b+1),2)+
                                pow((mjj_jes[mold-1][b]/100)*h0new.GetBinContent(b+1),2))
                err_tot0 = sqrt(pow(h0new.GetBinError(b+1),2)+pow(err_sys_tot0,2))
                #print "Value: ", round(h0new.GetBinContent(b+1),4), " stat:",round(h0new.GetBinError(b+1),4),"smear:",round((mjj_smear[mold-1]/100)*h0new.GetBinContent(b+1),4),"jer:",round((mjj_jer[mold-1][b]/100)*h0new.GetBinContent(b+1),4),"jes:",round((mjj_jes[mold-1][b]/100)*h0new.GetBinContent(b+1),4),"cor:",round((mjj_cor_err[mold-1][b]/100)*h0new.GetBinContent(b+1),4),"total:",round(err_tot0,4) #,"jeseta:",round((mjj_etajes[m-1][b]/100)*h0new.GetBinContent(b+1),4)
                h0newsys.SetBinContent(b+1,h0new.GetBinContent(b+1))
                h0newsys.SetBinError(b+1,err_sys_tot0)
                h0newall.SetBinContent(b+1,h0new.GetBinContent(b+1))
                h0newall.SetBinError(b+1,err_tot0)
            new_hists+=[h0newall]
            new_hists+=[h0newsys]
            h0new.SetLineColor(6)
            h0new.SetMarkerColor(6)
            h0newall.SetLineColor(6)
            h0newsys.SetLineColor(6)
        
        ### PLOT ###

        if doRatio:
            if doDataData:
                if mx<10:
                  ratio(h0all,h0old,True)
                  ratio(h0sys,h0old,True)
                  ratio(h0,h0old,True)
                else:
                  continue
                ratio(h2,h1)
                ratio(h3,h1)
                ratio(h1_alt,h1)
                for i in range(lambdasetlength):
                    ratio(h1_alt2[i],h1)
                ratio(h1,h1)
            else:
                ratio(h0all,h1)
                ratio(h0sys,h1)
                ratio(h0,h1)
                if compareNewData:
                    ratio(h0newall,h1)
                    ratio(h0newsys,h1)
                    ratio(h0new,h1)
                if mx<10:
                  ratio(h0oldall,h1)
                  ratio(h0oldsys,h1)
                  ratio(h0old,h1)
                ratio(h2,h1)
                ratio(h3,h1)
                ratio(h1_alt,h1)
                for i in range(lambdasetlength):
                    ratio(h1_alt2[i],h1)
                ratio(h1,h1)

        h0all.Add(TF1("offset",str(offsets[mx-1]),1,16))
        h0sys.Add(TF1("offset",str(offsets[mx-1]),1,16))
        h0.Add(TF1("offset",str(offsets[mx-1]),1,16))
        if compareNewData:
            h0newall.Add(TF1("offset",str(offsets[mx-1]),1,16))
            h0newsys.Add(TF1("offset",str(offsets[mx-1]),1,16))
            h0new.Add(TF1("offset",str(offsets[mx-1]),1,16))
        if mx<10:
          h0oldall.Add(TF1("offset",str(offsets[mx-1]),1,16))
          h0oldsys.Add(TF1("offset",str(offsets[mx-1]),1,16))
          h0old.Add(TF1("offset",str(offsets[mx-1]),1,16))
        h1.Add(TF1("offset",str(offsets[mx-1]),1,16))
        if alt3:
            h2.Add(TF1("offset",str(offsets[mx-1]),1,16))
            h3.Add(TF1("offset",str(offsets[mx-1]),1,16))
        else:
            h3.Apply(TF2("offset",str(offsets[mx-1])+"+y",1,16))
        h1_alt.Add(TF1("offset",str(offsets[mx-1]),1,16))
        for i in range(lambdasetlength):
            h1_alt2[i].Add(TF1("offset",str(offsets[mx-1]),1,16))

        if thicker:
            h0all.SetLineWidth(2)
            h0sys.SetLineWidth(2)
            h0.SetLineWidth(2)
            if compareNewData:
                h0newall.SetLineWidth(2)
                h0newsys.SetLineWidth(2)
                h0new.SetLineWidth(2)
            if mx<10:
              h0oldall.SetLineWidth(2)
              h0oldsys.SetLineWidth(2)
              h0old.SetLineWidth(2)
            h1.SetLineWidth(2)
            h2.SetLineWidth(2)
            h3.SetLineWidth(2)
            h1_alt.SetLineWidth(2)
            for i in range(lambdasetlength):
                h1_alt2[i].SetLineWidth(2)

        if compareNewData:
            h0all.SetLineWidth(2)
            h0sys.SetLineWidth(2)
            h0.SetLineWidth(2)

        h1_alt.SetLineWidth(3)
        for i in range(lambdasetlength):
            h1_alt2[i].SetLineWidth(3)

        h1.SetLineColor(kBlack)
        #h1.SetLineStyle(2)
        #h2.SetLineColor(kRed)
        h2.SetLineColor(15)
        h2.SetFillColor(10)
        #h3.SetLineColor(kRed)
        h3.SetLineColor(15)
        #h3.SetFillColor(kRed)
        h3.SetFillColor(15)
        h1_alt.SetLineStyle(9)
        h1_alt.SetLineColor(2)
        h1_alt2[0].SetLineStyle(2)
        h1_alt2[0].SetLineColor(4)
        if theories_plot:
            h1_alt2[1].SetLineStyle(3)
            h1_alt2[1].SetLineColor(kMagenta+2)
            h1_alt2[2].SetLineStyle(5)
            h1_alt2[2].SetLineColor(6)
            if lambdasetlength>3:
              h1_alt2[3].SetLineStyle(6)
              h1_alt2[3].SetLineColor(7)
            if lambdasetlength>4:
              h1_alt2[4].SetLineStyle(1)
              h1_alt2[4].SetLineColor(8)
            if lambdasetlength>5:
              h1_alt2[5].SetLineStyle(7)
              h1_alt2[5].SetLineColor(14)
        h1.GetYaxis().SetRangeUser(0.02,offsets[-1]+0.05)
        if theories_plot:
            h1.GetYaxis().SetRangeUser(0,offsets[-1])
        h1.GetXaxis().SetTitle("#chi_{dijet}") # = exp(|y_{1}-y_{2}|)
        h1.GetXaxis().SetTitleFont(42);
        h1.GetYaxis().SetTitleFont(42);
        h1.GetXaxis().SetRangeUser(1,16)
        if doRatio:
            if doDataData:
                if run2010new:
                    h1.GetYaxis().SetTitle("42X 2010 Data / 38X 2010 Data (1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet})")
                else:
                    h1.GetYaxis().SetTitle("2011 Data / 2010 Data (1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet})")
            else:
                h1.GetYaxis().SetTitle("Data / Theory (1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet})")
        else:    
            h1.GetYaxis().SetTitle("1/#sigma_{dijet} d#sigma_{dijet}/d#chi_{dijet}")
        h1.GetYaxis().SetTitleOffset(1.4)
        h1.GetXaxis().SetTitleOffset(0.8)
        if theories_plot:
            h1.GetYaxis().SetTitleOffset(1.5)
            h1.GetXaxis().SetTitleOffset(1.0)
        h1.GetYaxis().SetTitleSize(0.05)
        h1.GetYaxis().SetLabelSize(0.04)
        h1.GetXaxis().SetTitleSize(0.05)
        h1.GetXaxis().SetLabelSize(0.04)
        h1.GetXaxis().SetTickLength(0.02)

        #ybinning=array.array('d')
        #for i in range(mass_bins_max):
        #    ybinning.append(offsets[i]+0.0125)
        #    ybinning.append(offsets[i]+0.025)
        #ybinning.append(offsets[-1])
        #h1.GetYaxis().Set(len(ybinning)-1,ybinning)
        #binlabel="0"
        #for i in range(len(ybinning)):
        #    h1.GetYaxis().SetBinLabel(i+1,binlabel)
        #    if binlabel=="0":
        #        binlabel="0.125"
        #    else:
        #        binlabel="0"

        if alt3a:
            h1graph=TGraphAsymmErrors(h1)
            new_hists+=[h1graph]
            for b in range(h1graph.GetXaxis().GetNbins()):
                h1graph.SetPoint(b,h1.GetBinCenter(b+1),h1.GetBinContent(b+1))
                h1graph.SetPointEYlow(b,h1.GetBinContent(b+1)-h2.GetBinContent(b+1))
                h1graph.SetPointEYhigh(b,h3.GetBinContent(b+1)-h1.GetBinContent(b+1))
            #h1graph.SetLineColor(kRed)
            h1graph.SetLineColor(15)
            #h1graph.SetFillColor(kRed)
            h1graph.SetFillColor(15)
        
        #if weightedBinCenter:
        #    if m==1:
        #        h1.Draw("axis")
        #    for b in range(h3.GetN()):
        #        x1,y1=(ROOT.Double(),ROOT.Double())
        #        h3.GetPoint(b,x1,y1)
        #        for i in range(len(chi_binnings[m-1])-1):
        #            if x1>chi_binnings[m-1][i] and x1<chi_binnings[m-1][i+1]:
        #                x1=weighted_bin_centers[i]
        #        h3.SetPoint(b,x1,y1)
        #    h3.Draw("cfsame")
        #    
        #    h1_altgraph=TGraph(h1_alt)
        #    new_hists+=[h1_altgraph]
        #    for b in range(h1_alt.GetXaxis().GetNbins()):
        #        h1_altgraph.SetPoint(b,weighted_bin_centers[b],h1_alt.GetBinContent(b+1))
        #    h1_altgraph.Draw("lsame")
        #    
        #    h1_alt2graph=TGraph(h1_alt2)
        #    new_hists+=[h1_alt2graph]
        #    for b in range(h1_alt2.GetXaxis().GetNbins()):
        #        h1_alt2graph.SetPoint(b,weighted_bin_centers[b],h1_alt2.GetBinContent(b+1))
        #    h1_alt2graph.Draw("lsame")
        #    
        #    h1graph=TGraph(h1)
        #    new_hists+=[h1graph]
        #    for b in range(h1.GetXaxis().GetNbins()):
        #        h1graph.SetPoint(b,weighted_bin_centers[b],h1.GetBinContent(b+1))
        #    h1graph.Draw("csame")
        #    
        #    h0graph=TGraphAsymmErrors(h0)
        #    new_hists+=[h0graph]
        #    for b in range(h0.GetXaxis().GetNbins()):
        #        h0graph.SetPoint(b,weighted_bin_centers[b],h0.GetBinContent(b+1))
        #        h0graph.SetPointEXlow(b,weighted_bin_centers[b]-chi_bins[m-1][b])
        #        h0graph.SetPointEXhigh(b,chi_bins[m-1][b+1]-weighted_bin_centers[b])
        #    h0graph.Draw("pzsame")
        #    
        #    h0sysgraph=TGraphAsymmErrors(h0sys)
        #    new_hists+=[h0sysgraph]
        #    for b in range(h0sys.GetXaxis().GetNbins()):
        #        h0sysgraph.SetPoint(b,weighted_bin_centers[b],h0sys.GetBinContent(b+1))
        #        h0sysgraph.SetPointEXlow(b,0)
        #        h0sysgraph.SetPointEXhigh(b,0)
        #    h0sysgraph.Draw("esame")
        #
        #    h0allgraph=TGraphAsymmErrors(h0all)
        #    new_hists+=[h0allgraph]
        #    for b in range(h0all.GetXaxis().GetNbins()):
        #        h0allgraph.SetPoint(b,weighted_bin_centers[b],h0all.GetBinContent(b+1))
        #        h0allgraph.SetPointEXlow(b,weighted_bin_centers[b]-chi_bins[m-1][b])
        #        h0allgraph.SetPointEXhigh(b,chi_bins[m-1][b+1]-weighted_bin_centers[b])
        #    h0allgraph.Draw("zsame")
        #else:
        if True:
            if first:
                h1.Draw("axis")
                first=False
            if not doDataData:
                if alt3a:
                    h1graph.Draw("e2")
                elif alt3:
                    h3.Draw("histsame")
                    h2.Draw("histsame")
                else:
                    h3.Draw("cfsame")
                if m>100:
                    if addLambda and not compareNewData:
                        if theories_plot:
                            if lambdasetlength==6:
                                h1_alt2[4].Draw("histsame")
                                h1_alt2[3].Draw("histsame")
                                h1_alt2[1].Draw("histsame")
                                h1_alt2[2].Draw("histsame")
                                h1_alt2[5].Draw("histsame")
                                h1_alt2[0].Draw("histsame")
                            else:
                              for i in range(lambdasetlength):
                                h1_alt2[i].Draw("histsame")
                        else:
                            h1_alt2[0].Draw("histsame")
                    if alt2:
                        h1_alt.Draw("histsame")
                    else:
                        h1_alt.Draw("histlsame")
                    if alt1:
                        h1_alt.SetMarkerStyle(25)
                        h1_alt.SetMarkerSize(0.7)
                        h1_alt.Draw("histpsame")
                #if alt2:
                #    h1.Draw("histsame")
                #else:
                #    h1.Draw("histcsame")
                #if alt1:
                #    h1.SetMarkerStyle(2)
                #    h1.SetMarkerSize(0.7)
                #    h1.Draw("histpsame")
                h1.Draw("axissame")
            else:
                if not doRatio:
                  if mx<10:
                    h0old.Draw("psame")
                    h0oldsys.Draw("e1x0same")
                    h0oldall.Draw("esame")
                else:
                    h1.SetLineColor(2)
                    h1.Draw("histlsame")
                    h1.Draw("axissame")
            if doRatio:
                h0sys.SetMarkerSize(0.0001)
                h0.SetMarkerSize(0.0001)
                if compareNewData:
                    h0newsys.SetMarkerSize(0.0001)
                    h0new.SetMarkerSize(0.0001)
            else:
                if compareNewData:
                    h0newsys.SetMarkerSize(0)
            h0.Draw("psame")
            if doRatio:
                h0sys.Draw("e1x0same")
            h0all.Draw("esame")
            if compareNewData and mx>5:
                h0new.Draw("psame")
                if doRatio:
                    h0newsys.Draw("e1x0same")
                h0newall.Draw("esame")

        ### LABELS ###

        if doRatio:
            ylabel=offsets[mx-1]*0.122+0.250
            if mx==7: ylabel+=0.035
            if mx==8: ylabel+=0.070
        else:
            ylabel=offsets[mx-1]*1.30+0.192
            if mx==7: ylabel+=0.030
            if mx==8: ylabel+=0.040
        if doRatio:
            ylabel=offsets[mx-1]*0.112+0.241
            if mx==7: ylabel+=0.000
            if mx==8: ylabel+=0.035
            if mx==9: ylabel+=0.070
        else:
            if compareNewData:
                ylabel=offsets[mx-1]*1.12+0.183
                if mx==7: ylabel+=0.01
                if mx==8: ylabel+=0.03
                if mx==9: ylabel+=0.03
            else:
                ylabel=offsets[mx-1]*1.21+0.188
                if mx==7: ylabel+=0.000
                if mx==8: ylabel+=0.030
                if mx==9: ylabel+=0.040


        #if mx==1: title="0.25 < #font[72]{M_{jj}} < 0.35"
        #if mx==2: title="0.35 < #font[72]{M_{jj}} < 0.5"
        #if mx==3: title="0.5 < #font[72]{M_{jj}} < 0.65"
        #if mx==4: title="0.65 < #font[72]{M_{jj}} < 0.85"
        #if mx==5: title="0.85 < #font[72]{M_{jj}} < 1.1"
        #if mx==6: title="1.1 < #font[72]{M_{jj}} < 1.4"
        #if mx==7: title="1.4 < #font[72]{M_{jj}} < 1.8"
        #if mx==8: title="1.8 < #font[72]{M_{jj}} < 2.2"
        #if mx==9: title="2.2 < #font[72]{M_{jj}}( < 2.8)"
        #if mx==10: title="#font[72]{M_{jj}} > 2.8"

        if mx==1: title="0.4 < #font[72]{M_{jj}} < 0.6"
        if mx==2: title="0.6 < #font[72]{M_{jj}} < 0.9"
        if mx==3: title="0.9 < #font[72]{M_{jj}} < 1.2"
        if mx==4: title="1.2 < #font[72]{M_{jj}} < 1.5"
        if mx==5: title="1.5 < #font[72]{M_{jj}} < 1.9"
        if mx==6: title="1.9 < #font[72]{M_{jj}} < 2.4"
        if mx==7: title="2.4 < #font[72]{M_{jj}} < 3.0"
        if mx==8: title="#font[72]{M_{jj}} > 3.0"

        if mx==1: title="0.4 < #font[72]{M_{jj}} < 0.6"
        if mx==2: title="0.6 < #font[72]{M_{jj}} < 0.8"
        if mx==3: title="0.8 < #font[72]{M_{jj}} < 1.0"
        if mx==4: title="1.0 < #font[72]{M_{jj}} < 1.2"
        if mx==5: title="1.2 < #font[72]{M_{jj}} < 1.5"
        if mx==6: title="1.5 < #font[72]{M_{jj}} < 1.9"
        if mx==7: title="1.9 < #font[72]{M_{jj}} < 2.4"
        if mx==8: title="2.4 < #font[72]{M_{jj}} < 3.0"
        if mx==9: title="#font[72]{M_{jj}} > 3.0"

        #if offsets[m-1]==0: title+=" TeV"
        #elif offsets[m-1]<0: title+=" TeV ("+str(offsets[m-1])+")"
        #else: title+=" TeV (+"+str(offsets[m-1])+")"
        
        title+=" TeV"
        if offsets[mx-1]==0: titleo=""
        elif offsets[mx-1]<0: titleo="("+str(offsets[mx-1])+")"
        else: titleo="(+"+str(offsets[mx-1])+")"

        if theories_plot:
          l=TLegend(0.30,0.74,1.0,0.74,title)
          if theories_plot2:
            l=TLegend(0.25,0.74,1.0,0.74,title)
          l.SetTextSize(0.035)
          l.SetFillStyle(0)
          l.Draw("same")
          new_hists+=[l]
        else:
          l=TLegend(0.55,ylabel,1.0,ylabel-0.005,title)
          l.SetTextSize(0.03)
          l.SetFillStyle(0)
          l.Draw("same")
          new_hists+=[l]

          lo=TLegend(0.84,ylabel,1.4,ylabel+0.01,titleo)
          lo.SetTextSize(0.03)
          lo.SetFillStyle(0)
          lo.Draw("same")
          new_hists+=[lo]

    if theories_plot:

        if doPaper:
            l5=TLegend(0.35,0.91,1.0,0.90,"CMS")
        elif doPreliminary:
            l5=TLegend(0.25,0.91,1.0,0.90,"CMS Preliminary")
        else:
            l5=TLegend(0.35,0.91,1.0,0.90,"")
        l5.SetTextSize(0.035)
        l5.SetFillStyle(0)
        l5.Draw("same")
        new_hists+=[l5]
         
        l5=TLegend(0.32,0.86,1.0,0.85,"#sqrt{s} = 7 TeV")
        l5.SetTextSize(0.035)
        l5.SetFillStyle(0)
        l5.Draw("same")
        new_hists+=[l5]
         
        if not doDataData:
            if run2010new:
                l=TLegend(0.32,0.81,1.0,0.80,"L = 36 pb^{-1}")
            else:
                l=TLegend(0.32,0.81,1.0,0.80,"L = 2.2 fb^{-1}")
                if compareNewData:
                    l=TLegend(0.32,0.81,1.0,0.80,"")
                elif combineNew2011Data or useNewData:
                    l=TLegend(0.32,0.81,1.0,0.80,"L = 5.0 fb^{-1}")
            l.SetTextSize(0.035)
            l.SetFillStyle(0)
            l.Draw("same")
            new_hists+=[l]

        if addLambda:
            l2=TLegend(0.54,0.5,0.95,0.95,"")
        else:
            l2=TLegend(0.52,0.5,0.95,0.,"")
        l2.SetTextSize(0.035)
        if alt4:
            l2.AddEntry(h0,"Data","p")
        else:
            if doDataData:
                if doRatio:
                    if run2010new:
                        l2.AddEntry(h0,"42X 2010 Data / 38X 2010 Data","lep")
                    else:
                        l2.AddEntry(h0,"2011 Data / 2010 Data","lep")
                else:
                    if run2010new:
                        l2.AddEntry(h0,"42X 2010 Data (36 pb^{-1})","lep")
                    else:
                        l2.AddEntry(h0,"2011 Data (2.2 fb^{-1})","lep")
            else:
                if compareNewData:
                  if combineNew2011Data or useNewData:
                    l2.AddEntry(h0,"Data 5.0 fb^{-1}","p")
                  else:
                    l2.AddEntry(h0,"Data 2.2 fb^{-1}","p")
                else:
                    l2.AddEntry(h0,"Data","lep")
        if compareNewData:
            l2.AddEntry(h0new,"2012 Data 5.1 fb^{-1}","lep")
        #l2.AddEntry(h1,"QCD prediction","l")
        #l2.AddEntry(h3,"Theory uncertainty","f")
        if not doDataData:
            l2.AddEntry(h3,"QCD prediction #sqrt{s} = 7 TeV","f")
            if addLambda and not compareNewData:
                if theories_plot:
                  if lambdaset==0:
                    #l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (NLO)","l")
                    #l2.AddEntry(h1_alt2[0],"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (NLO)","l")
                    #l2.AddEntry(h1_alt2[1],"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (LO)","l")
                    #l2.AddEntry(h1_alt2[2],"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (LO)","l")
                    #l2.AddEntry(h1_alt2[3],"#Lambda_{V/A}^{#font[122]{+}} = 7 TeV (LO)","l")
                    #l2.AddEntry(h1_alt2[4],"#Lambda_{V/A}^{#font[122]{-}} = 7 TeV (LO)","l")
                    #l2.AddEntry(h1_alt2[5],"#Lambda_{(V-A)}^{#pm} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{VV/AA}^{#font[122]{+}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[4],"#Lambda_{VV/AA}^{#font[122]{-}} = 7 TeV (LO)","l")
                    #l2.AddEntry(h1_alt2[5],"#Lambda_{RL}^{#pm} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[5],"#Lambda_{(V-A)}^{#pm}   = 7 TeV (LO)","l")
                  if lambdaset==1:
                    l2.AddEntry(h1_alt,"#Lambda_{LL}^{#font[122]{+}} = 5 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL}^{#font[122]{+}} = 6 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL}^{#font[122]{+}} = 7 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL}^{#font[122]{+}} = 8 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{LL}^{#font[122]{+}} = 9 TeV (NLO)","l")
                  if lambdaset==2:
                    l2.AddEntry(h1_alt,"#Lambda_{LL}^{#font[122]{-}} = 6 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL}^{#font[122]{-}} = 7 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL}^{#font[122]{-}} = 8 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL}^{#font[122]{-}} = 10 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{LL}^{#font[122]{-}} = 12 TeV (NLO)","l")
                  if lambdaset==3:
                    l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{#font[122]{+}} = 5 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL/RR}^{#font[122]{+}} = 6 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL/RR}^{#font[122]{+}} = 8 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{LL/RR}^{#font[122]{+}} = 9 TeV (LO)","l")
                  if lambdaset==4:
                    l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL/RR}^{#font[122]{-}} = 9 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL/RR}^{#font[122]{-}} = 11 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL/RR}^{#font[122]{-}} = 13 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{LL/RR}^{#font[122]{-}} = 15 TeV (LO)","l")
                  if lambdaset==5:
                    l2.AddEntry(h1_alt,"#Lambda_{V/A}^{#font[122]{+}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{V/A}^{#font[122]{+}} = 8 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{V/A}^{#font[122]{+}} = 9 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{V/A}^{#font[122]{+}} = 10 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{V/A}^{#font[122]{+}} = 11 TeV (LO)","l")
                  if lambdaset==6:
                    l2.AddEntry(h1_alt,"#Lambda_{V/A}^{#font[122]{-}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{V/A}^{#font[122]{-}} = 9 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{V/A}^{#font[122]{-}} = 11 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{V/A}^{#font[122]{-}} = 13 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{V/A}^{#font[122]{-}} = 15 TeV (LO)","l")
                  if lambdaset==7:
                    l2.AddEntry(h1_alt,"#Lambda_{(V-A)}^{#pm} = 5 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[0],"#Lambda_{(V-A)}^{#pm} = 6 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{(V-A)}^{#pm} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{(V-A)}^{#pm} = 8 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{(V-A)}^{#pm} = 9 TeV (LO)","l")
                else:
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL/RR}^{#font[122]{-}} = 7 TeV (NLO)","l")
            else:
              l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{+} = 7 TeV (NLO)","l")
        else:
            if not doRatio:
              if mx<10:
                if run2010new:
                    l2.AddEntry(h0old,"38X 2010 Data (36 pb^{-1})","lep")
                else:
                    l2.AddEntry(h0old,"2010 Data (36 pb^{-1})","lep")
        #l2.AddEntry(h1,"NLO + NPC","l")
        #l2.AddEntry(h3,"#sigma(#mu_{F},#mu_{R},PDF,NPC)","f")
        #l2.AddEntry(h5,"Pythia D6T","l")s
        #l2.AddEntry(h6,"Pythia Z2","l")
        l2.SetFillStyle(0)
        l2.Draw("same")
        new_hists+=[l2]
        if alt4:
            if addLambda:
                l3=TLegend(0.275,0.85,0.276,0.96,"")
            else:
                l3=TLegend(0.575,0.85,0.576,0.96,"")
            l3.SetTextSize(0.035)
            l3.AddEntry(h0,"","le")
            l3.AddEntry(h0,"","")
            l3.AddEntry(h0,"","")
            l3.AddEntry(h0,"","")
            l3.SetFillStyle(0)
            l3.Draw("same")
            new_hists+=[l3]


    else:
        if doPaper:
            l5=TLegend(0.74,0.94,1.0,0.94,"CMS")
        elif doPreliminary:
            l5=TLegend(0.65,0.94,1.0,0.94,"CMS Preliminary")
        else:
            l5=TLegend(0.65,0.94,1.0,0.94,"")
        l5.SetTextSize(0.035)
        l5.SetFillStyle(0)
        l5.Draw("same")
        new_hists+=[l5]
         
        l5=TLegend(0.7,0.91,1.0,0.91,"#sqrt{s} = 7 TeV")
        l5.SetTextSize(0.035)
        l5.SetFillStyle(0)
        #l5.Draw("same")
        new_hists+=[l5]
         
        if not doDataData:
            if run2010new:
                l=TLegend(0.7,0.88,1.0,0.88,"L = 36 pb^{-1}")
            else:
                l=TLegend(0.7,0.88,1.0,0.88,"L = 2.2 fb^{-1}")
                if compareNewData:
                    l=TLegend(0.7,0.88,1.0,0.88,"")
                elif combineNew2011Data or useNewData:
                    l=TLegend(0.7,0.88,1.0,0.88,"L = 5.0 fb^{-1}")
            l.SetTextSize(0.035)
            l.SetFillStyle(0)
            l.Draw("same")
            new_hists+=[l]

        if addLambda:
            l2=TLegend(0.23,0.85,0.76,0.96,"")
        else:
            l2=TLegend(0.23,0.86,0.76,0.95,"")
        l2.SetTextSize(0.035)
        if alt4:
            l2.AddEntry(h0,"Data","p")
        else:
            if doDataData:
                if doRatio:
                    if run2010new:
                        l2.AddEntry(h0,"42X 2010 Data / 38X 2010 Data","lep")
                    else:
                        l2.AddEntry(h0,"2011 Data / 2010 Data","lep")
                else:
                    if run2010new:
                        l2.AddEntry(h0,"42X 2010 Data (36 pb^{-1})","lep")
                    else:
                        l2.AddEntry(h0,"2011 Data (2.2 fb^{-1})","lep")
            else:
                if compareNewData:
                  if combineNew2011Data or useNewData:
                    l2.AddEntry(h0,"2011 Data 5.0 fb^{-1}","lep")
		  else:
                    l2.AddEntry(h0,"2011 Data 2.2 fb^{-1}","lep")
                else:
                    l2.AddEntry(h0,"Data","lep")
        if compareNewData:
            l2.AddEntry(h0new,"2012 Data 5.1 fb^{-1}","lep")
        #l2.AddEntry(h1,"QCD prediction","l")
        #l2.AddEntry(h3,"Theory uncertainty","f")
        if not doDataData:
            l2.AddEntry(h3,"QCD prediction","f")
            #l2.AddEntry(h1_alt,"#Lambda_{LL/RR}^{#font[122]{+}} = 7 TeV (NLO)","l")
            if addLambda and not compareNewData:
                if theories_plot:
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL}^{#font[122]{-}} = 7 TeV (NLO)","l")
                    l2.AddEntry(h1_alt2[1],"#Lambda_{LL}^{+} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[2],"#Lambda_{LL}^{#font[122]{-}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[3],"#Lambda_{V}^{+} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[4],"#Lambda_{V}^{#font[122]{-}} = 7 TeV (LO)","l")
                    l2.AddEntry(h1_alt2[5],"#Lambda_{VA}^{#pm} = 7 TeV (LO)","l")
                else:
                    l2.AddEntry(h1_alt2[0],"#Lambda_{LL}^{#font[122]{-}} = 7 TeV (NLO)","l")
        else:
            if not doRatio:
              if mx<10:
                if run2010new:
                    l2.AddEntry(h0old,"38X 2010 Data (36 pb^{-1})","lep")
                else:
                    l2.AddEntry(h0old,"2010 Data (36 pb^{-1})","lep")
        #l2.AddEntry(h1,"NLO + NPC","l")
        #l2.AddEntry(h3,"#sigma(#mu_{F},#mu_{R},PDF,NPC)","f")
        #l2.AddEntry(h5,"Pythia D6T","l")s
        #l2.AddEntry(h6,"Pythia Z2","l")
        l2.SetFillStyle(0)
        l2.Draw("same")
        new_hists+=[l2]
        if alt4:
            if addLambda:
                l3=TLegend(0.275,0.85,0.276,0.96,"")
            else:
                l3=TLegend(0.575,0.85,0.576,0.96,"")
            l3.SetTextSize(0.035)
            l3.AddEntry(h0,"","le")
            l3.AddEntry(h0,"","")
            l3.AddEntry(h0,"","")
            l3.AddEntry(h0,"","")
            l3.SetFillStyle(0)
            l3.Draw("same")
            new_hists+=[l3]

    if doRatio:
        c.Print(prefix+"nlo_final_ratio-"+jetalgo+jettype+".ps")
        os.system("ps2pdf "+prefix+"nlo_final_ratio-"+jetalgo+jettype+".ps "+prefix+"nlo_final_ratio-"+jetalgo+jettype+".pdf")
    elif doDataData:
        c.Print(prefix+"nlo_final_data-"+jetalgo+jettype+".ps")
        os.system("ps2pdf "+prefix+"nlo_final_data-"+jetalgo+jettype+".ps "+prefix+"nlo_final_data-"+jetalgo+jettype+".pdf")
    elif compareNewData:
        c.Print(prefix+"nlo_final_compdata-"+jetalgo+jettype+".ps")
        os.system("ps2pdf "+prefix+"nlo_final_compdata-"+jetalgo+jettype+".ps "+prefix+"nlo_final_compdata-"+jetalgo+jettype+".pdf")
    elif combineNewData:
        c.Print(prefix+"nlo_final_adddata-"+jetalgo+jettype+".ps")
        os.system("ps2pdf "+prefix+"nlo_final_adddata-"+jetalgo+jettype+".ps "+prefix+"nlo_final_adddata-"+jetalgo+jettype+".pdf")
        f = TFile(prefix+"unsmeared_data_hists"+jetalgo+jettype+".root","RECREATE")
        for hist in data_hists:
            hist.Write()
        f.Close()
    else:
        print "Number of unsmeared data events:"
        print unsmeared_data_events
        if doPaper:
            c.Print(prefix+"nlo_final-"+jetalgo+jettype+"-paper.ps")
            os.system("ps2pdf "+prefix+"nlo_final-"+jetalgo+jettype+"-paper.ps "+prefix+"nlo_final-"+jetalgo+jettype+"-paper.pdf")
        else:
            c.Print(prefix+"nlo_final-"+jetalgo+jettype+".ps")
            os.system("ps2pdf "+prefix+"nlo_final-"+jetalgo+jettype+".ps "+prefix+"nlo_final-"+jetalgo+jettype+".pdf")
        f = TFile(prefix+"unsmeared_data_hists"+jetalgo+jettype+".root","RECREATE")
        for hist in data_hists:
            hist.Write()
        f.Close()
        f = TFile(prefix+"notunsmeared_data_hists"+jetalgo+jettype+".root","RECREATE")
        for hist in data_hists2:
            hist.Write()
        f.Close()

    if not doRatio and not theories_plot:
        row=0
        if True:
          for m in reversed(range(1,mass_bins_max+1)):
            print table["Mjj"][row]+" \\\\"
            for b in range(len(chi_bins[m-1])-1):
                line=table["chi"][row]
                line+=" & $\pm "+"{n:1.2f}".format(n=table["JES"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["JER"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["JERtails"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["Unsmear"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["SIM"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["TotalData"][row]*100.)+"$"
                line+=" \\\\"
                print line
                row+=1
            print "\\hline"
        print ""

        row=0
        if True:
          for m in reversed(range(1,mass_bins_max+1)):
            print table["Mjj"][row]+" \\\\"
            for b in range(len(chi_bins[m-1])-1):
                line=table["chi"][row]
                line+=" & ${+"+"{n:1.2f}".format(n=table["Scale+"][row]*100.)+"}{-"+"{n:1.2f}".format(n=table["Scale-"][row]*100.)+"}$"
                line+=" & ${+"+"{n:1.2f}".format(n=table["PDF+"][row]*100.)+"}{-"+"{n:1.2f}".format(n=table["PDF-"][row]*100.)+"}$"
                line+=" & ${+"+"{n:1.2f}".format(n=table["NPC+"][row]*100.)+"}{-"+"{n:1.2f}".format(n=table["NPC-"][row]*100.)+"}$"
                line+=" & ${+"+"{n:1.2f}".format(n=table["TotalTheory+"][row]*100.)+"}{-"+"{n:1.2f}".format(n=table["TotalTheory-"][row]*100.)+"}$"
                line+=" \\\\"
                print line
                row+=1
            print "\\hline"
        print ""

        row=0
        if True:
          for m in reversed(range(1,mass_bins_max+1)):
            print table["Mjj"][row]+" \\\\"
            for b in range(len(chi_bins[m-1])-1):
                line=table["chi"][row]
                #line+=" & "+"{n:1.1f}".format(n=table["chi_center"][row])
                line+=" & "+"{n:1.0f}".format(n=table["N_raw"][row])
                line+=" & "+"{n:1.3f}".format(n=table["c_unsmear"][row])
                #line+=" & "+"{n:1.1f}".format(n=table["N_unsmeared"][row])
                line+=" & "+"{n:1.4f}".format(n=table["N_normalized"][row])
                line+=" & "+"{n:1.4f}".format(n=table["N_qcd_normalized"][row])
                line+=" & "+"{n:1.4f}".format(n=table["N_qcdci_normalized"][row])
                line+=" \\\\"
                print line
                row+=1
            print "\\hline"

        row=0
        if True:
          for m in reversed(range(1,mass_bins_max+1)):
            print table["Mjj"][row]+" \\\\"
            for b in range(len(chi_bins[m-1])-1):
                total_up=sqrt(pow(table["N_normalized"][row]*table["Stat"][row],2)+
                           pow(table["N_normalized"][row]*table["TotalData"][row],2)+
                           pow(table["N_normalized"][row]*table["TotalTheory+"][row],2))/table["N_normalized"][row]
                total_down=sqrt(pow(table["N_normalized"][row]*table["Stat"][row],2)+
                           pow(table["N_normalized"][row]*table["TotalData"][row],2)+
                           pow(table["N_normalized"][row]*table["TotalTheory-"][row],2))/table["N_normalized"][row]
                line=table["chi"][row]
                line+=" & $\pm "+"{n:1.2f}".format(n=table["Stat"][row]*100.)+"$"
                line+=" & $\pm "+"{n:1.2f}".format(n=table["TotalData"][row]*100.)+"$"
                line+=" & ${+"+"{n:1.2f}".format(n=table["TotalTheory+"][row]*100.)+"}{-"+"{n:1.2f}".format(n=table["TotalTheory-"][row]*100.)+"}$"
                line+=" & ${+"+"{n:1.2f}".format(n=total_up*100.)+"}{-"+"{n:1.2f}".format(n=total_down*100.)+"}$"
                line+=" \\\\"
                print line
                row+=1
            print "\\hline"

        row=0
        print "dijet angular distributions (arXiv:1102.2020)"
        print "CMS data 2.2/fb"
        for m in reversed(range(1,mass_bins_max+1)):
            print "(YRAP(P=3)+YRAP(P=4))/2 : < 1.1"
            print "M(P=3_4) : "+table["Mjj"][row]+" GeV"
            print "RE: P P --> JET JET X"
            print "SQRT(S) : 7000.0 GeV"
            print "x: CHI = exp(|Y1-Y2|)"
            print "y: (1/SIG)*D(SIG)/DCHI"
            print "xlow xhigh y +-stat +-sys"
            for b in range(len(chi_bins[m-1])-1):
                print table["chi_low"][row]+" "+table["chi_high"][row]+\
                " "+"{n:1.4f}".format(n=table["N_normalized"][row])+\
                " +-"+"{n:1.4f}".format(n=table["Stat"][row]*table["N_normalized"][row])+\
                " +-"+"{n:1.4f}".format(n=table["TotalData"][row]*table["N_normalized"][row])
                row+=1
            print ""

        row=0
        print "NLO QCD + non perturbative corretions"
        for m in reversed(range(1,mass_bins_max+1)):
            print "|y_boost| = |y1+y2|/2 < 1.1"
            print "dijet invariant mass: "+table["Mjj"][row]+" GeV"
            print "x: dijet chi = exp(|y1-y2|)"
            print "y: 1/chi dsigma/dchi"
            print "xlow xhigh y +sys -sys"
            for b in range(len(chi_bins[m-1])-1):
                print table["chi_low"][row]+" "+table["chi_high"][row]+\
                " "+"{n:1.4f}".format(n=table["N_qcd_normalized"][row])+\
                " +"+"{n:1.4f}".format(n=table["TotalTheory+"][row]*table["N_qcd_normalized"][row])+\
                " -"+"{n:1.4f}".format(n=table["TotalTheory-"][row]*table["N_qcd_normalized"][row])
                row+=1
            print ""

    c.WaitPrimitive()
