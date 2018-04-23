' ###############
' PROPERTIES
'

cancelTransition As Boolean

ExLuggName As String

expDir As FolderItem

ExpName As String

idDict As Dictionary

luggIndex As pLuggage

LuggName As String

maskName As String

templateLines() As String




' ###############
' MAIN FUNCTION
'
Sub Transition()
  
  '#pragma BoundsChecking False
  '#pragma BreakOnExceptions True
  
  Dim LibraryDir,ResDir As String
  
  Dim genTempStr As String
  
  
  Dim tx As FolderItem
  Dim xx As FolderItem
  
  ErrorList.DeleteAllRows()
  
  TBB_Save.Enabled = False
  TBB_Save.Refresh()
  TBB_Save.Visible = False
  
  
  Dim p As String = app.ConfDir + "data/tags.da"
  Dim f As FolderItem = GetURLFolderItem(p,2)
  TagDataLB.DeleteAllRows()
  Dim sx,txx(),x As String
  Dim iix,nnx As Integer
  txx = OpenFile(f).Split(";")
  nnx = txx.Ubound
  if nnx>-1 Then
    for iix=0 to nnx
      sx = txx(iix)
      
      If sx.StartsWith("EF::") Then
        Dim xt() As String
        x = sx.Replace("EF::","")
        Dim kt() As String = x.Split("::")
        
        if kt.Ubound >= 1 Then
          TagDataLB.AddRow(kt(0).ReplaceAll("&SEM",":"))
          TagDataLB.Cell(TagDataLB.LastIndex,1) = kt(1)
        End If
        if kt.Ubound = 2 Then
          TagDataLB.Cell(TagDataLB.LastIndex,1) = kt(2)
          TagDataLB.CellTag(TagDataLB.LastIndex,1) = "EF::" + kt(2)
        End If
        'ElseIf s.StartsWith("p_=") Then
        'x = s.ReplaceAll("p_=","")
        'p_ = x
      End If
      
    next
  End If
  
  
  if expDir <> Nil Then
    
    // generate 'export_energyclass.cbcm' idDict
    generateTemplateDict(App.MaskDir.Child("export_energyclass.cbcm"))
    if idDict = Nil Then
      MsgBox "Bitte legen Sie vorher die Datei 'export_energyclass.cbcm' unter '" + App.maskDir.AbsolutePath + "' an und starten Sie den Vorgang neu."
      Exit
    End If
    
    
    
    Dim expFolderPath As String = app.TmpFolder.URLPath + "EXPORT_" + expDir.name.ReplaceAll(":","_")
    expFolderPath = EncodeUrlPath(expFolderPath)
    Dim expFolder As FolderItem = app.TmpFolder.Child("EXPORT_" + expDir.name.ReplaceAll(":","_")) 'GetFolderItem(expFolderPath,2)
    
    Dim walk As FolderItem 
    walk = expDir
    
    //If Explicit then collect this files only (SFD Query for files)
    
    Dim oFiles() As FolderItem
    
    if ExportExplicitBox.Value = True Then
      if luggIndex<>Nil Then
        Dim retS() As pProduct = luggIndex.DirInfo_GetProducts("explicit","ARTNR","EXPORTFLAG")
        Dim tProd As pProduct
        Dim ri,rn,optCount As Integer
        Dim pDir As FolderItem
        if retS.Ubound>-1 Then
          rn = retS.Ubound
          For ri=0 to rn
            
            tProd = retS(ri)
            if tProd <> Nil Then
              pDir = GetURLFolderItem(luggIndex.relPathFile.URLPath + tProd.ArtRelPath.ReplaceAll(" ","%20")+"/",2)
              oFiles.Append pDir
              'LibList.addDir(pDir,tProd.ArtName,tProd.ArtNr,tProd.ArtFlags,tProd.ArtAction,tProd.ArtDelivery,tProd.ArtNr,tProd.mExportFlags)
              optCount = optCount + 1
              
            End If
          Next
        End If
        
      end if
      
    end if
    
    Dim foldercopied As Boolean = False
    Dim MD As New LsCopyWin
    MD.Show()
    if ExportExplicitBox.Value = True Then
      if oFiles.Ubound>-1 Then 
        MD.oFiles = oFiles
      End If
    End If
    MD.CopyFilesFolder(expdir,expFolder)
    
    '#if TargetWin32
    'MD.ShowModal()
    '#endif
    MD.ShowModal()
    
    'while not MD.returnValue>0 
    'app.DoEvents()
    'Wend
    'MD.Close()
    
    select case MD.ReturnValue
    case 1 //YES
      
      'expFolder.Launch()
      'exit
      
      walk = expFolder
      
    case 2 //NO
      'SelText =  ts
      
      MsgBox "Vorgang abgebrochen!" '+ EndOfLine + EndOfLine + "Daten werden nun wieder vom Server verarbeitet."
      
      Exit
      
      'walk = expDir
      
    case 3 //Alternate
      
    end select
    
    Dim mProd As pProduct
    
    Dim ii,n,c As Integer
    Dim et,exp As String
    Dim lugName As String
    Dim lugP1,lugP2,lugP3,lugP4,lugP5 As String
    
    Dim luggGlobalBT As String
    Dim luggGBT(4) As String
    
    n = walk.Count
    ExpField.Text = ""
    TBB_Save.Enabled = False
    WalkerPanel.Enabled = True
    WalkerScroll.max = n
    WalkerScroll.min = 1
    WalkerLbl.Text = "1 / " + str(n)
    Dim slug As String = expDir.name
    slug = slug.Replace(".lugg",".ilugg")
    Dim luggCat As String = OpenFile(expDir.Child(slug))
    
    Dim ExpPicCount,ExpDownloadCount As Integer
    Dim ExpDiscount As String
    
    Dim GlobalValueStr As String
    
    
    Dim VorkasseFactor,EKFactor,VKFactor As Double = 0.00
    Dim shippingCharge As Double = 0.0
    Dim minPriceFormula,FKFormular As String
    Dim useFK As Boolean = False
    Dim rabattMArray(-1),faktorVKMArray(-1) As String
    
    Dim z,zt(),zm,tz() As String
    luggCat = luggCat.ReplaceAll(REALbasic.EndOfLine,"")
    zt = luggCat.split(";")
    if zt.Ubound > - 1 Then
      Dim xic,xnc As Integer
      xnc = zt.Ubound
      for xic=0 to xnc
        z = zt(xic)
        z = z.ReplaceAll(Chr(9),"")
        z = z.ReplaceAll(Chr(13),"")
        z = z.ReplaceAll(Chr(10),"")
        //MsgBox(z)
        if z.StartsWith("NAME=") Then
          z = z.Replace("NAME=","")
          lugName = z
          ExLuggName = z
          'MsgBox(z)
        Elseif z.StartsWith("ExpName=") Then
          z = z.Replace("ExpName=","")
          ExpName = z
        Elseif z.StartsWith("VORKASSEFAKT=") Then
          z = z.Replace("VORKASSEFAKT=","")
          VorkasseFactor = val(z)
        elseif z.StartsWith("FAKTEK=") then
          z = z.Replace("FAKTEK=","")
          'FaktorEKField.Text = z
          EKFactor = val(z)
        elseif z.StartsWith("FAKTVK=") then
          z = z.Replace("FAKTVK=","")
          'FaktorVKField.Text = z
          VKFactor = val(z)
        elseif z.StartsWith("MinPriceFormular=") then
          z = z.Replace("MinPriceFormular=","")
          minPriceFormula = z
        elseif z.StartsWith("FKFormular=") then
          z = z.Replace("FKFormular=","")
          'z= z.Replace(",",".")
          FKFormular = z
        elseif z.StartsWith("useFKFormular=") then
          z = z.Replace("useFKFormular=","")
          'z= z.Replace(",",".")
          if boolstrRev(z) Then
            UseFK = True
          Else
            UseFK = False
          End If
          
        elseif z.StartsWith("shippingCharge=") then
          z = z.Replace("shippingCharge=","")
          z= z.Replace(",",".")
          shippingCharge = val(z)
          
          
        Elseif z.StartsWith("DISCOUNT=") Then
          z = z.Replace("DISCOUNT=","")
          if not (z="") Then
            ExpDiscount = z
          Else
            ExpDiscount = "0"
          End If
        Elseif z.StartsWith("PicCount=") Then
          z = z.Replace("PicCount=","")
          ExpPicCount=val(z)
        Elseif z.StartsWith("DownCount=") Then
          z = z.Replace("DownCount=","")
          ExpDownloadCount=val(z)
        Elseif z.StartsWith("GlobalValues=") Then
          z = z.Replace("GlobalValues=","")
          
          z = z.ReplaceAll("&SEM",":")
          z = z.ReplaceAll("&SM",";")
          z = z.ReplaceAll("&EOL","")
          z = z.ReplaceAll("'","""")
          GlobalValueStr = z
          
        ElseIf z.StartsWith("P1Value=") Then
          z = z.Replace("P1Value=","")
          z = ReplaceCTRLChars(z)
          lugP1 = z
          luggGBT(0) = z
        ElseIf z.StartsWith("P2Value=") Then
          z = z.Replace("P2Value=","")
          z = ReplaceCTRLChars(z)
          lugP2 = z
          luggGBT(1) = z
        ElseIf z.StartsWith("P3Value=") Then
          z = z.Replace("P3Value=","")
          z = ReplaceCTRLChars(z)
          lugP3 = z
          luggGBT(2) = z
        ElseIf z.StartsWith("P4Value=") Then
          z = z.Replace("P4Value=","")
          z = ReplaceCTRLChars(z)
          lugP4 = z
          luggGBT(3) = z
        ElseIf z.StartsWith("P5Value=") Then
          z = z.Replace("P5Value=","")
          z = ReplaceCTRLChars(z)
          lugP5 = z
          luggGBT(4) = z
          
          
        Elseif z.StartsWith("RABATT=") then
          z = z.Replace("RABATT=","")
          DIm zs() As String = z.split("§")
          Dim zi,zn As Integer
          zn=zs.Ubound
          if zn>-1 then
            For zi=0 to zn
              'RabattListBox.AddRow(zs(zi))
              zs(zi) = zs(zi).Replace(",",".")
              rabattMArray.Append (zs(zi))
            Next
          End If
          'rPriceField.Text = z
          'RabattPriceMenu.Caption = z
        Elseif z.StartsWith("UFAKTVK=") then
          z = z.Replace("UFAKTVK=","")
          DIm zs() As String = z.split("§")
          Dim zi,zn As Integer
          zn=zs.Ubound
          if zn>-1 then
            For zi=0 to zn
              'RabattListBox.AddRow(zs(zi))
              zs(zi) = zs(zi).Replace(",",".")
              faktorVKMArray.Append (zs(zi))
            Next
          End If
          
          
        End If
      next
    End If
    
    Dim pi,pn As Integer
    Dim pxout As String
    pn = ExpPicCount
    For pi=1 to pn
      If pi>1Then
        pxout=pxout+FeldTrenner+"p_image."+str(pi-1)
      Elseif pi=1 Then
        pxout="p_image"
      End If
    next
    
    
    ErrorList.AddRow("Beginne Export: " + Lieferant_Menu.Caption + " ...")
    ErrorList.AddRow("Erlaubt Bildfelder: " + str(ExpPicCount) + "; Erlaubte Downloadfelder: " + str(ExpDownloadCount))
    ErrorList.AddRow("Zu bearbeitende Dateien: " + str(n))
    
    ErrorList.AddRow(">>>>")
    
    
    Dim ExportList() As String
    
    
    
    'MsgBox pxout
    'ExportList.Append "XTSOL" + FeldTrenner + "action" + FeldTrenner + "p_model" + FeldTrenner + "p_stock" + FeldTrenner +_
    '"p_sorting" + FeldTrenner + "p_shipping" + FeldTrenner + "p_tpl" + FeldTrenner + "p_manufacturer" + FeldTrenner +_
    '"p_fsk18" + FeldTrenner + "p_priceNoTax" + FeldTrenner + "p_priceNoTax.1" + FeldTrenner + "p_priceNoTax.2" +_
    'FeldTrenner + "p_minPrice.de" + FeldTrenner + "p_tax" + FeldTrenner + "p_status" + FeldTrenner + "p_weight" +_
    'FeldTrenner + "p_ean" + FeldTrenner + "p_disc" + FeldTrenner + "p_opttpl" + FeldTrenner + "p_vpe" + FeldTrenner +_
    '"p_vpe_status" + FeldTrenner + "p_vpe_value" + FeldTrenner + "p_name.de" + FeldTrenner + "p_desc.de" + FeldTrenner +_
    '"p_shortdesc.de" + FeldTrenner + "p_meta_title.de" + FeldTrenner + "p_meta_desc.de" + FeldTrenner +_
    '"p_meta_key.de" + FeldTrenner + "p_keywords.de" + FeldTrenner + "p_url.de" + FeldTrenner +_
    '"p_cat.0" + FeldTrenner + "p_cat.1" + FeldTrenner + "p_cat.2" + FeldTrenner + "p_cat.3" + FeldTrenner + "p_cat.4" + FeldTrenner + "p_google.de" + FeldTrenner + "p_specifications.de" +_
    'FeldTrenner + "p_downloads.de" + FeldTrenner + "p_movies.de"+ FeldTrenner + pxout + "$EOL$"'Chr(13) + Chr(10)'EndOfLine.Windows'Chr(13) + Chr(10) 'EndOfLine
    
    ExportList.Append "XTSOL" + FeldTrenner + "action" + FeldTrenner + "p_model" + FeldTrenner + "p_stock" + FeldTrenner +_
    "p_sorting" + FeldTrenner + "p_shipping" + FeldTrenner + "p_tpl" + FeldTrenner + "p_manufacturer" + FeldTrenner +_
    "p_fsk18" + FeldTrenner + "p_priceNoTax" + FeldTrenner + "p_priceNoTax.1" + FeldTrenner + "p_priceNoTax.2" +_
    FeldTrenner + "p_minPrice.de" + FeldTrenner + "p_tax" + FeldTrenner + "p_status" + FeldTrenner + "p_weight" +_
    FeldTrenner + "p_ean" + FeldTrenner + "p_disc" + FeldTrenner + "p_opttpl" + FeldTrenner + "p_vpe" + FeldTrenner +_
    "p_vpe_status" + FeldTrenner + "p_vpe_value" + FeldTrenner + "p_name.de" + FeldTrenner + "p_desc.de" + FeldTrenner +_
    "p_shortdesc.de" + FeldTrenner + "p_meta_title.de" + FeldTrenner + "p_meta_desc.de" + FeldTrenner +_
    "p_meta_key.de" + FeldTrenner + "p_keywords.de" + FeldTrenner + "p_url.de" + FeldTrenner +_
    "p_cat.0" + FeldTrenner + "p_cat.1" + FeldTrenner + "p_cat.2" + FeldTrenner + "p_cat.3" + FeldTrenner + "p_cat.4" + FeldTrenner + "p_google.de" + FeldTrenner +_
    "products_energy_efficiency" + FeldTrenner + "products_energy_efficiency_pict" + FeldTrenner + "products_energy_efficiency_text"+ Feldtrenner +_
    "p_movies.de"+ FeldTrenner + pxout + "$EOL$"'Chr(13) + Chr(10)'EndOfLine.Windows'Chr(13) + Chr(10) 'EndOfLine
    
    
    
    'ExpField.Text = exp
    
    Dim wRefreshInterval As Integer
    
    If WalkerScroll.Max < 1024 Then
      wRefreshInterval = 10
    Elseif WalkerScroll.Max >= 1024 Then
      wRefreshInterval = 100
    Elseif WalkerScroll.Max >= 2048 Then
      wRefreshInterval = 200
    End If
    
    
    Dim oofX As FolderItem
    Dim oof As FolderItem
    Dim oofXD As FolderItem
    Dim oofXY As FolderItem
    
    Dim action, p_model,p_shipping,p_manufacturer,p_priceNoTax, p_priceNoTax1, p_priceNoTax2,p_minPriceDe,p_tax,p_status,p_weight,p_ean,p_disc,p_image,p_image1,p_image2,p_image3,ü_images,_
    p_name,p_desc,p_shortdesc,p_meta_title,p_meta_desc,p_meta_key,p_keywords,p_url, p_cat1,p_cat2,p_cat3,p_cat4,p_cat5,p_google,p_specifications,p_downloads,p_movies ,_
    yt1,yt2,ytdesc1,ytdesc2, down1,down2,down3,downdesc1,downdesc2,downdesc3,p_welcome,p_artlisting,zGEW,p_priceGen, p_priceSonder,p_priceOut,p_ImpTechData, exportFlag,_
    p_EnergyClass, p_EnergyClassPict, p_EnergyClassText As String '= ""
    Dim pxTECHDATA As String 
    Dim pEKFactor, pVKFactor As String
    
    Dim ArtThisText, OverwriteBT, code, k,m , xt ,xtdl ,ss , oZGEW , pImagesOut , gDelimtter As String
    Dim ArtWelcomeState,ic,nc , ax,xi,xn,AWS As Integer = -1
    Dim b As Boolean
    Dim hasTechs As Boolean = False
    Dim hasSupply As Boolean = False
    Dim hasImpTechData As Boolean = False
    Dim UseSonderPreis As Boolean = False
    Dim continueExport As Boolean = False
    
    
    
    App.ExportTask = True
    
    
    //implement package export walker -> copy luggage to local storage and then export and walk through
    
    
    
    for ii=1 to n
      
      if cancelTransition = True Then
        
        MsgBox "Export Vorgang wurde vom Benutzer abgebrochen!"
        
        Exit For ii
      End If
      
      If (ii Mod wRefreshInterval) Mod 2 = 0 Then 
        WalkerScroll.value = ii
        WalkerLbl.Text = str(ii) + " / " + str(n)
        WalkerScroll.Refresh()
      End If
      'MsgBox(walk.item(ii).URLPath)
      'MsgBox("'"+walk.item(ii).name+"'")
      If walk.item(ii).name.EndsWith(".prod") Then
        
        
        
        'Dim luggGlobalBT As String
        
        
        If not (walk.item(ii).Name.StartsWith("X_") Or walk.item(ii).Name.StartsWith(".") Or walk.item(ii).Name.StartsWith("$") or walk.item(ii).name = ".prod") Then
          
          //##############################
          // Garbage Collector
          oofX = Nil
          oof = Nil
          oofXD = Nil
          oofxY = NIL
          action=""
          exportFlag=""
          p_model=""
          p_shipping=""
          p_manufacturer=""
          p_priceGen=""
          p_priceOut=""
          p_priceSonder=""
          p_priceNoTax=""
          p_priceNoTax1=""
          p_priceNoTax2=""
          p_minPriceDe=""
          p_tax=""
          p_status=""
          p_weight=""
          p_ean=""
          p_disc=""
          p_image=""
          p_image1=""
          p_image2=""
          p_image3=""
          ü_images=""
          p_name=""
          p_desc=""
          p_shortdesc=""
          p_meta_title=""
          p_meta_desc=""
          p_meta_key=""
          p_keywords=""
          p_url=""
          p_cat1=""
          p_cat2=""
          p_cat3=""
          p_cat4=""
          p_cat5=""
          p_google=""
          p_specifications=""
          p_downloads=""
          p_movies=""
          p_EnergyClass=""
          p_EnergyClassPict=""
          p_EnergyClassText=""
          yt1=""
          yt2=""
          ytdesc1=""
          ytdesc2=""
          down1=""
          down2=""
          down3=""
          downdesc1=""
          downdesc2=""
          downdesc3=""
          p_welcome=""
          p_artlisting=""
          zGEW=""
          ArtWelcomeState = -1
          ArtThisText =""
          OverwriteBT =""
          code =""
          k=""
          m=""
          b=False
          xt=""
          xtdl =""
          ic=-1
          nc=-1
          ax=-1
          ss=""
          xi=-1
          xn=-1
          oZGEW=""
          AWS=-1
          pImagesOut =""
          p_ImpTechData = ""
          pxTECHDATA = ""
          gDelimtter = ""
          hasTechs = False
          hasSupply = False
          hasImpTechData = False
          mProd = New pProduct
          continueExport = False
          
          mProd.mVorkasseFactor = VorkasseFactor
          mProd.p_MinPriceFormula = minPriceFormula
          mProd.mFKFormular = FKFormular
          mProd.mUseLuggFK = UseFK
          mProd.p_shippingCharge = shippingCharge
          
          
          dim DownBase(-1) As String
          Dim pImages(-1) As String
          Dim kt(-1) As String
          Dim t(-1) As String
          Dim o(-1) As String
          Dim sxt(-1) As String
          
          TechDataLB.DeleteAllRows
          SuppDataLB.DeleteAllRows
          
          //########################################
          //########################################
          
          'If not (ExpName="") Then 
          'p_manufacturer = ExpName
          'Else
          'p_manufacturer = lugName
          'End If
          
          
          'oof = GetURLFolderItem(walk.item(ii).URLPath + walk.item(ii).name,2)
          oof = walk.item(ii).Child(walk.item(ii).name)
          if oof<>nil and oof.Exists=True Then
            
            
            
            
            code = OpenFile(oof)
            xt = code
            xt = xt.ReplaceAll(REALbasic.EndOfLine,"")
            
            
            if (xt.Contains("RABATT=")=False) Or (code.Contains("RABATT=")=False) Then
              ErrorList.AddRow("ÜBERSPRUNGEN Datei (" + str(ii) + ") - " + oof.name + " -> Kein Herstellerrabatt gefunden! Fehlerhafte Preiskalkulation")
              
              Continue For ii
            End If
            
            
            if xt.Contains("gVD=") Then
              
              
              xtdl = xt.left(7).Replace("gVD=","")
              gDelimtter =xtdl
              t = xt.Split(gDelimtter)
            Else
              
              t = xt.Split(";")
              gDelimtter=";"
            End If
            if t.Ubound > -1 Then
              
              nc = t.Ubound
              for ic=0 to nc
                k = t(ic)
                k = k.ReplaceAll(Chr(9),"")
                k = k.ReplaceAll(Chr(13),"")
                k = k.ReplaceAll(Chr(10),"")
                
                if k.StartsWith("NAME=") Then
                  k = k.Replace("NAME=","")
                  p_name = k.StripLineEndings().Trim()
                  WalkerLbl.Text = str(ii) + " / " + str(n) + EndOfLine + p_name + EndOfLine + p_model
                  
                  
                Elseif k.StartsWith("CAT0=") Then
                  k = k.Replace("CAT0=","")
                  if not ((k="...")or(k="")) Then p_cat1 = k
                Elseif k.StartsWith("CAT1=") Then
                  k = k.Replace("CAT1=","")
                  if not ((k="...")or(k="")) Then p_cat2 = k
                Elseif k.StartsWith("CAT2=") Then
                  k = k.Replace("CAT2=","")
                  if not ((k="...")or(k="")) Then p_cat3 = k
                Elseif k.StartsWith("CAT3=") Then
                  k = k.Replace("CAT3=","")
                  if not ((k="...")or(k="")) Then p_cat4 = k
                Elseif k.StartsWith("CAT4=") Then
                  k = k.Replace("CAT4=","")
                  if not ((k="...")or(k="")) Then p_cat5 = k
                ElseIf k.StartsWith("ARTNR=") Then
                  k = k.Replace("ARTNR=","")
                  p_model = k.StripLineEndings().Trim()
                  WalkerLbl.Text = str(ii) + " / " + str(n) + EndOfLine + p_name + EndOfLine + p_model
                  
                ElseIf k.StartsWith("MANUFACTURER=") Or (k.StartsWith("MANUFACTURER") and k.contains("LASTEDIT")) Then
                  Dim tkx As String
                  if k.contains("LASTEDIT") Then
                    Dim ksx() As String = k.Split("LASTEDIT")
                    Dim iks,ikn As Integer
                    ikn = ksx.Ubound
                    if ikn>-1 Then
                      tkx = ksx(0)
                      k = tkx
                    End If
                  End If
                  k = k.Replace("MANUFACTURER=","").Replace("MANUFACTURER","")
                  p_manufacturer = k.StripLineEndings().Trim()
                  'WalkerLbl.Text = str(ii) + " / " + str(n) + EndOfLine + p_name + EndOfLine + p_model
                  
                  
                ElseIf k.StartsWith("ARTLISTING=") Then
                  k = k.Replace("ARTLISTING=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL",EndOfLine)
                  k = k.ReplaceAll("&SEM",":")
                  p_artlisting = k
                ElseIf k.StartsWith("ARTWELCOMESTATE=") Then
                  k = k.Replace("ARTWELCOMESTATE=","")
                  ArtWelcomeState = val(k)
                ElseIf k.StartsWith("WELCOMETHISTEXT=") Then
                  k = k.Replace("WELCOMETHISTEXT=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL",EndOfLine)
                  k = k.ReplaceAll("&SEM",":")
                  ArtThisText = k
                ElseIf k.StartsWith("WELCOMETEXT=") Then
                  k = k.Replace("WELCOMETEXT=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL",EndOfLine)
                  k = k.ReplaceAll("&SEM",":")
                  p_welcome = k
                ElseIf k.StartsWith("OVERWRITESTDBT=") Then
                  k = k.Replace("OVERWRITESTDBT=","")
                  OverwriteBT = k
                ElseIf k.StartsWith("SHORTDESC=") Then
                  k = k.Replace("SHORTDESC=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL","")
                  p_shortdesc = k
                  
                ElseIf k.StartsWith("DESC=") Then
                  k = k.Replace("DESC=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL","")
                  p_desc = k
                  
                  'ElseIf k.StartsWith("OUTPRICE=") Then
                  'k = k.Replace("OUTPRICE=","")
                  'p_priceOut = k
                  ''k = k.Replace(",",".")
                  ''p_priceNoTax = k
                  ''p_priceNoTax1 = k
                  ''p_priceNoTax2 = k
                  'ElseIf k.StartsWith("SPRICE=") Then
                  'k = k.Replace("SPRICE=","")
                  'p_priceSonder = k
                  ''p_priceNoTax = k
                  ''p_priceNoTax1 = k
                  ''p_priceNoTax2 = k
                  'ElseIf k.StartsWith("USESPRICE=") Then
                  'k = k.Replace("USESPRICE=","")
                  'If k = "TRUE" Then UseSonderPreis = True
                  '
                  'ElseIf k.StartsWith("MPRICE=") Then
                  'k = k.Replace("MPRICE=","")
                  'k = k.Replace(",",".")
                  'p_minPriceDe = k
                  'ElseIf k.StartsWith("RPRICE=") Then
                  'k = k.Replace("RPRICE=","")
                  ''ArtMPrice=k
                  
                ElseIf k.StartsWith("PRICE=") Then
                  k = k.Replace("PRICE=","")
                  k = k.Replace(",",".")
                  'ArtPrice=k
                  mProd.p_listprice = val(k)
                  
                ElseIf k.StartsWith("SPRICE=") Then
                  k = k.Replace("SPRICE=","")
                  k = k.Replace(",",".")
                  mProd.p_SonderPreis = val(k)
                ElseIf k.StartsWith("USESPRICE=") Then
                  k = k.Replace("USESPRICE=","")
                  if k = "TRUE" Then
                    mProd.mUseSonderpreis = True
                  End If
                ElseIf k.StartsWith("USEVORKASSE=") Then
                  k = k.Replace("USEVORKASSE=","")
                  if k = "TRUE" Then
                    mProd.mUseVorkasse = True
                  End If
                ElseIf k.StartsWith("USERFAKTVK=") Then
                  k = k.Replace("USERFAKTVK=","")
                  k = k.Replace(",",".")
                  
                  if k = "Standard" Then
                    mProd.mUseNewVKFaktor = False
                    pVKFactor = k
                  Elseif k.contains(":") Then
                    Dim nFac(-1) As String = k.split(":")
                    DIm xF As String = nFac(0)
                    DIm fi,fn As Integer
                    DIm tf As String
                    pVKFactor = xF
                    fn = faktorVKMArray.Ubound
                    if fn>-1 Then
                      For fi=0 to fn
                        tf = faktorVKMArray(fi)
                        if tf.Contains(xF) Then
                          
                          mProd.mUseNewVKFaktor = True
                          mProd.mUVKFactor = val(tf)
                          
                          pVKFactor = tf
                        End If
                      Next
                    End If
                    
                    'FaktorVKMenu.Caption = k
                  Else
                    mProd.mUseNewVKFaktor = True
                    mProd.mUVKFactor = val(k)
                    pVKFactor = k
                    
                  End If
                  
                ElseIf k.StartsWith("USESHIPPINGCHARGE=") Then
                  k = k.Replace("USESHIPPINGCHARGE=","")
                  if k = "TRUE" Then
                    'mProd.mUseSonderpreis = True
                    mProd.mUseShippingCharge = True
                    'ArtSPrice = k
                  Else
                    mProd.mUseShippingCharge = False
                  End If
                  
                ElseIf k.StartsWith("PRICEBASE=") Then //PRICEBASE=ListPrice//ShopEK
                  k = k.Replace("PRICEBASE=","")
                  If k = "ListPrice" Then
                    mProd.mUseListAsShopEK=True
                  ElseIf k = "NettoPrice" Then
                    mProd.mUseListAsShopEK=False
                  ENd If
                  
                ElseIf k.StartsWith("RABATT=") Then
                  k = k.Replace("RABATT=","")
                  k =  k.Replace(",",".")
                  
                  if k.contains(":") Then
                    Dim nFac(-1) As String = k.split(":")
                    DIm xF As String = nFac(0)
                    DIm fi,fn As Integer
                    DIm tf As String
                    pEKFactor = xF
                    fn = rabattMArray.Ubound
                    if fn>-1 Then
                      For fi=0 to fn
                        tf = rabattMArray(fi)
                        if tf.Contains(xF) Then
                          mProd.p_PriceRabatt = val(tf)
                          pEKFactor = tf
                          'RabattPriceMenu.Caption = tf
                        End If
                      Next
                    End If
                  Else
                    pEKFactor = "1"
                    mProd.p_PriceRabatt = val(k)
                    pEKFactor = k
                  End If
                  
                  
                  
                Elseif k.StartsWith("MANLINK=") Then
                  k = k.Replace("MANLINK=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&SEM",":")
                  p_url = k.StripLineEndings().Trim()
                Elseif k.StartsWith("SEARCHKEYS=") Then
                  k = k.Replace("SEARCHKEYS=","")
                  p_keywords = k.StripLineEndings().Trim()
                Elseif k.StartsWith("METATITLE=") Then
                  k = k.Replace("METATITLE=","")
                  p_meta_title = k.StripLineEndings().Trim()
                Elseif k.StartsWith("METADESC=") Then
                  k = k.Replace("METADESC=","")
                  p_meta_desc = k.StripLineEndings().Trim()
                Elseif k.StartsWith("METAKEYS=") Then
                  k = k.Replace("METAKEYS=","")
                  p_meta_key = k.StripLineEndings().Trim()
                Elseif k.StartsWith("ZGEW=") Then
                  k = k.Replace("ZGEW=","")
                  if not k.Contains("Keine") Then zGEW = k
                Elseif k.StartsWith("ACTION=") Then
                  k = k.Replace("ACTION=","")
                  action = k
                  
                  if action = "ignore" then
                    //break out of this prod analysis
                    
                    ErrorList.AddRow("ÜBERSPRUNGEN Datei (" + str(ii) + ") - " + oof.name + " -> action: ignore")
                    
                    Continue For ii
                    
                  End If
                  
                Elseif k.StartsWith("EXPORTFLAG=") Then
                  k = k.Replace("EXPORTFLAG=","")
                  exportFlag = k
                  
                  if (exportFlag = "ignore") Or (exportFlag = "editing") then
                    //break out of this prod analysis
                    
                    ErrorList.AddRow("ÜBERSPRUNGEN Datei (" + str(ii) + ") - " + oof.name + " -> ExportFlag: " + exportFlag)
                    
                    Continue For ii
                    
                  Elseif (exportFlag = "explicit") and (ExportExplicitBox.Value = True) then
                    
                    continueExport = True
                    
                  Elseif (exportFlag = "explicit") and (ExportExplicitBox.Value = False) then
                    
                    continueExport = True
                    
                  Elseif ((exportFlag = "export") Or (exportFlag = "")) and (ExportExplicitBox.Value = False) Then
                    
                    continueExport = True
                    
                  End If
                  
                Elseif k.StartsWith("DELSTAT=") Then
                  k = k.Replace("DELSTAT=","")
                  'MsgBox(k)
                  p_shipping = str(val(k)+1)
                elseif k.StartsWith("EAN=") Then
                  k = k.Replace("EAN=","")
                  p_ean = k.StripLineEndings().Trim()
                  
                  
                elseif k.StartsWith("PIC.") Then
                  o = k.split("=")
                  k = k.Replace("PIC.","")
                  'Dim ax As Integer
                  If o.Ubound = 1 Then
                    if not (o(1)="") Then
                      //Collect Picture Data
                      pImages.Append(o(0)+"="+o(1))
                      
                    end if
                    
                  End If
                  
                  
                  
                elseif k.StartsWith("DOWNLOAD.") Then
                  k = k.Replace("DOWNLOAD.","")
                  o = k.split("=")
                  If o.Ubound = 1 Then
                    ax = val(o(0))
                    if ax > -1 Then
                      
                      DownBase.Append(o(1).StripLineEndings().Trim())
                      'mDownloadBase.AddField( bx(0),bx(1),bx(2),str(ax) )
                      
                    End If
                  End If
                  
                  
                elseif k.StartsWith("YT1=") Then
                  k = k.Replace("YT1=","")
                  yt1= k.StripLineEndings().Trim()
                elseif k.StartsWith("YTDESC1=") Then
                  k = k.Replace("YTDESC1=","")
                  ytdesc1 = k.StripLineEndings().Trim()
                elseif k.StartsWith("YT2=") Then
                  k = k.Replace("YT2=","")
                  yt2 = k.StripLineEndings().Trim()
                elseif k.StartsWith("YTDESC2=") Then
                  k = k.Replace("YTDESC2=","")
                  ytdesc2 = k.StripLineEndings().Trim()
                elseif k.StartsWith("P_GOOGLE=") Then
                  k = k.Replace("P_GOOGLE=","")
                  p_google = k.StripLineEndings().Trim()
                  
                  
                  
                  
                  //#########################
                  //#########################
                  // Tech & Supp Fields
                  //#########################
                  //#########################
                elseif k.StartsWith("TECHDATA=") Then
                  k = k.Replace("TECHDATA=","")
                  UnWrappListData(TechDataLB,k)
                  pxTECHDATA = k
                  hasTechs = True
                  
                elseif k.StartsWith("SUPPDATA=") Then
                  k = k.Replace("SUPPDATA=","")
                  UnWrappListData(SuppDataLB,k)
                  hasSupply = True
                  
                elseif k.StartsWith("IMPTECHDATA=") Then
                  k = k.Replace("IMPTECHDATA=","")
                  k = k.ReplaceAll("&SM",";")
                  k = k.ReplaceAll("&EOL",EndOfLine)
                  k = k.ReplaceAll("&SEM",":")
                  p_ImpTechData = k
                  hasImpTechData = True
                  
                  'p_EnergyClass=""
                  'p_EnergyClassPict=""
                  'p_EnergyClassText=""
                elseif k.StartsWith("ENERGYCLASS=") Then 
                  k = k.Replace("ENERGYCLASS=","")
                  p_EnergyClass=k
                elseif k.StartsWith("ENERGYCLASSPICT=") Then
                  k = k.Replace("ENERGYCLASSPICT=","")
                  p_EnergyClassPict=k
                elseif k.StartsWith("ENERGYCLASSTEXT=") Then
                  k = k.Replace("ENERGYCLASSTEXT=","")
                  p_EnergyClassText=k
                End If
              next
              
              If (exportFlag = "") and (ExportExplicitBox.Value = False) Then continueExport = True
              if continueExport = False Then
                
                ErrorList.AddRow("ÜBERSPRUNGEN Datei (" + str(ii) + ") - " + oof.name + " -> Eigenschaften verhindern export")
                
                Continue For ii
                
              End If
              
              
              //###############
              //Price Stuff
              
              'mProd.mVorkasseFactor = VorkasseFactor
              '
              'mProd.mEKFactor = EKFactor
              '
              'mProd.mVKFactor = VKFactor
              '
              'mProd.p_MinPriceFormula = minPriceFormula
              '
              '
              'mProd.CalcPrices(mProd.p_PriceRabatt)
              '
              'p_minPriceDe =  Format(mProd.mShopMinPrice,"#.##")
              'p_minPriceDe =  p_minPriceDe.ReplaceAll(",",".")
              ''ShopEKField.Text = Format(mProd.mShopEK,"#.00")
              'p_priceNoTax = Format(mProd.mShopVK,"#.##")
              '
              'p_priceNoTax1 = p_priceNoTax.ReplaceAll(",",".")
              'p_priceNoTax2 = p_priceNoTax.ReplaceAll(",",".")
              
              //###############
              //###############
              //PriceCalculation V2
              //###############
              
              //herstellerrabatt
              Dim pxc As String = pEKFactor.Replace(",",".")
              
              if pxc.Contains(":") Then
                Dim ps() As String = pxc.split(":")
                pxc = ps(1)
              End If
              
              mProd.mEKFactor = val(pxc)
              mProd.p_PriceRabatt = val(pxc)
              
              //Nutzerrabatt (FaktoVK - vk-faktor.de)
              
              Dim txc As String = pVKFactor.Replace(",",".")
              
              if txc.Contains(":") Then
                Dim ts() As String = txc.split(":")
                txc = ts(1)
              End If
              
              mProd.mUseNewVKFaktor = True
              mProd.mUVKFactor = val(txc)
              
              mProd.CalcPrices(mProd.p_PriceRabatt)
              
              if mProd.p_outprice = mprod.mShopEK Then
                ErrorList.AddRow("ÜBERSPRUNGEN Datei (" + str(ii) + ") - " + oof.name + " -> Preisfehler -> VK = Netto EK")
                
                Continue For ii
              end if
              
              p_priceNoTax = Format(mProd.mRound(mProd.p_outprice),"#.##")
              p_priceNoTax1 = Format(mProd.mRound(mProd.p_outprice),"#.00").ReplaceAll(",",".")
              p_priceNoTax2 = Format(mProd.mRound(mProd.p_outprice),"#.00").ReplaceAll(",",".")
              
              p_minPriceDe = Format(mProd.mShopMinPrice,"#.00").ReplaceAll(",",".")
              'ShopEKField.Text = Format(mProd.mShopEK,"#.##")
              
              
              
              'outPriceField.Text = Format(mProd.p_outprice,"#.00")
              
              
              //###############
              //###############
              //###############
              //###############
              
              
              'if (ii=14) Or (ii=16) Or (ii=18) Then
              'Dim sxb As Boolean
              'sxb = True
              'End If
              
              'ss = "<!--details-->"
              
              if hasTechs = True Then //Check if file has got own TechSpecs
                ss = ss + GenerateListTablePrev(TechDataLB,mProd)
                
                //Generate EnergyClassText from TECHDATA with export_energyclass.cbcm
                If p_EnergyClass.Len>0Then
                  p_EnergyClassText = prod_generateEnergyTechData(pxTECHDATA) '""
                  if p_EnergyClassText.Len>0 Then
                    UnWrappListData(TechDataLB,p_EnergyClassText)
                    p_EnergyClassText = GenerateListTablePrev(TechDataLB,mProd)
                  End If
                Else
                  p_EnergyClassText = ""
                End If
              elseif hasImpTechData = True Then
                
                ss = ss.replaceAll("IMPTECHDATA=","")
                ss = ss + GenerateTableFromString(p_ImpTechData,mProd)
                
                'Else //Otherwise check if has .pimp TechSpecs
                'genTempStr = walk.item(ii).URLPath
                'genTempStr = genTempStr + walk.item(ii).name.Replace(".prod","")
                'genTempStr = genTempStr + "_TechSpecs.pimp"
                'oofx = GetURLFolderItem(genTempStr,2)
                'if (oofx<>nil) and (oofx.Exists=True) Then 
                'Dim tss As String
                'tss = OpenFileLatin(oofX).ReplaceAll("TECHSPECS-IMPORT=","")
                '
                ''tss = DecodeHTML(tss)
                '
                'tss = GenerateTableFromString(tss,mProd)
                '
                'ss = ss + tss
                ''ss = ss + GenerateListTablePrev(TechDataLB) // !!! - Needs to implemented
                'End If
                'genTempStr = ""
              End If
              
              //replace global Tokenz
              ss = ss.ReplaceAll("$Artikelname$",p_name)
              ss = ss.ReplaceAll("$HEADArtikelname$","<h2>"+p_name+"</h2>")
              ss = ss.ReplaceAll("$Artikelnumber$",p_model)
              //------
              ss = ss.ReplaceAll(gDelimtter,"")
              ss = ss.ReplaceAll("§+§","")
              ss = EncodeHTML(ss)
              
              'ss = ss + "<!--/details-->"
              
              p_specifications = ss
              
              
              Dim supplData As String
              
              if hasSupply = True Then
                supplData = "<h3>Zubeh&ouml;r</h3>" + GenerateListTablePrev(SuppDataLB,mProd)
              Else
                supplData = ""
              End If
              
              
              'p_downloads = "<!--attachments-->"<!--downloads-->""<!--details-->"
              
              '"DOWNLOAD."+str(downCount)+"="+downlink+"]["+downtitle+"]["+downtype+"]["+ArtName+"]["+downalt + gDelimtter
              
              Dim ai,an As Integer
              an = DownBase.Ubound
              
              Dim dpText,dpdText As String
              
              if an >-1 Then
                For ai=0 to an 
                  'if ai <= ExpDownloadCount -1 Then
                  sxt = DownBase(ai).Split("][")
                  'mCC(index).DownField.Text + "][" + mCC(index).DownDescField.Text + "][" + mCC(index).Voreinstellung_Menu.Caption + "][" + Str(mCC(index).mIndex)
                  'if sxt.Ubound>=4 Then
                  'p_downloads = p_downloads + "<div id=""p_downloads""><a href=""" + sxt(0) + """ target=""_blank""><img title=""Download " + sxt(2)+" - " + sxt(4) + """ alt=""Download"" src=""/images/download.jpg"" /></a>" + sxt(2)+" - " + sxt(4) + " " + sxt(1)+ "</div>"
                  
                  if sxt.Ubound>-1 Then
                    if sxt(0).contains("media/Links/") then sxt(0) = sxt(0).Replace("media/Links/","")
                    dpText = sxt(2)
                    dpdText = sxt(1)
                    Dim mDownURL As String = p_downMedia + sxt(0)
                    if not (mDownURL.Contains("media/Links/")) Then mDownURL = p_downMedia + mDownURL
                    
                    p_downloads = p_downloads + "<a href=""" + mDownURL + """ target=""_blank""><img title=""Download " + sxt(2) '<div id=""p_downloads"">
                    If sxt(1).Len>0 Then
                      p_downloads = p_downloads + " - " + sxt(1).ReplaceAll("$Artikelname$",p_name).ReplaceAll("$HEADArtikelname$","<h2>"+p_model+"</h2>").ReplaceAll("$Artikelnumber$",p_model) 
                    End If
                    p_downloads = p_downloads + """ alt=""Download"" src=""/images/download.jpg"" style=""vertical-align: middle;""/></a>" + sxt(2)
                    If sxt(1).Len>0 Then 
                      p_downloads = p_downloads + " - " + sxt(1).ReplaceAll("$Artikelname$",p_name).ReplaceAll("$HEADArtikelname$","<h2>"+p_model+"</h2>").ReplaceAll("$Artikelnumber$",p_model) ' + sxt(4) + " "
                    End If
                    'p_downloads = p_downloads +"</div>"
                    
                  End If
                  'Elseif ai > maxDownFieldCount -1 Then
                  '
                  'sxt  = DownBase(ai).Split("][")
                  'ErrorList.AddRow("[!!!] - Download("+str(ai) + "::"+p_model+") - >"+sxt(0) +"< konnte nicht hinzugefügt werden. ")
                  'End If
                  p_downloads = p_downloads + "<br />"
                next
              Else // Use .pimp Downloads
                genTempStr = walk.item(ii).URLPath
                genTempStr = genTempStr + walk.item(ii).name.Replace(".prod","")
                genTempStr = genTempStr + "_Downloads.pimp"
                oofXD = GetURLFolderItem(genTempStr,2)
                if oofXD<>Nil and oofXD.Exists=TRUE Then p_downloads = OpenFile(oofXD).ReplaceAll("DOWNLOAD-IMPORT=","")
                genTempStr = ""
              End If
              p_downloads = p_downloads.ReplaceAll(gDelimtter,"")
              'p_downloads = p_downloads + "<!--/downloads-->"
              
              if not ((yt1 = "") and (ytdesc1 = "")) Then
                '<a href="http://www.youtube.com/watch?v=Uibm_RQfZ-M" class="movie" title="Testmovie1" target="_blank">Testmovie1</a>
                p_movies = "<a href=""" + yt1 + " class=""movie"" title=""" + ytdesc1 + """ target=""_blank"">" + ytdesc1 + "</a>"
                if not ((yt2 = "") and (ytdesc2 = "")) Then
                  '<a href="http://www.youtube.com/watch?v=Uibm_RQfZ-M" class="movie" title="Testmovie1" target="_blank">Testmovie1</a>
                  p_movies = p_movies + "<br/><a href=""" + yt2 + " class=""movie"" title=""" + ytdesc2 + """ target=""_blank"">" + ytdesc2 + "</a>"
                End If
              Else // Use .pimp Youtube
                genTempStr = walk.item(ii).URLPath
                genTempStr = genTempStr + walk.item(ii).name.Replace(".prod","")
                genTempStr = genTempStr + "_Youtube.pimp"
                
                oofXY = GetURLFolderItem(genTempStr,2)
                if oofXY<>Nil and oofXY.Exists=TRUE Then p_movies = OpenFile(oofXY).ReplaceAll("YOUTUBE-IMPORT=","")
                
                genTempStr = ""
              End If
              p_movies = p_movies.ReplaceAll(gDelimtter,"")
              
              
              
              ozGEW = zGEW
              
              //p_outprice zu p_listprice geändert
              ozGEW = oZGEW.ReplaceAll( "5%LP" , Format((mProd.p_listprice*1.05)-mProd.p_listprice,"###,##0.00") )
              oZGEW = oZGEW.ReplaceAll( "10%LP",Format((mProd.p_listprice*1.1)-mProd.p_listprice,"###,##0.00") )
              
              
              
              //Add more tokenz
              
              'luggGlobalBT = "<div id=""p_info"">" + EndOfLine + luggGBT(0) + EndOfLine + luggGBT(1) + EndOfLine + luggGBT(2) + EndOfLine + luggGBT(3) + EndOfLine + luggGBT(4) + EndOfLine + "</div>"
              luggGlobalBT = EndOfLine + luggGBT(0) + EndOfLine + luggGBT(1) + EndOfLine + luggGBT(2) + EndOfLine + luggGBT(3) + EndOfLine + luggGBT(4) + EndOfLine
              luggGlobalBT = luggGlobalBT.ReplaceAll("$Artikelname$",p_name)
              luggGlobalBT = luggGlobalBT.ReplaceAll("$HEADArtikelname$","<h2>"+p_name+"</h2>")
              luggGlobalBT = luggGlobalBT.ReplaceAll("$Artikelnumber$",p_model)
              luggGlobalBT = luggGlobalBT.Replace("$BT-Text(3)$",luggGBT(3)) 
              luggGlobalBT = luggGlobalBT.Replace("$BT-Text(4)$",luggGBT(4))
              
              
              
              
              AWS = ArtWelcomeState
              Dim rps As String = "</h2><br/>" + ozGew + " &euro;. <br/>"
              dim tlgt As String
              
              
              If (AWS =1)Then //Global
                if not (ozgew="") Then
                  luggGlobalBT = ConvertEncoding(luggGlobalBT,Encodings.UTF8)
                  tlgt = luggGlobalBT
                  tlgt = ConvertEncoding(tlgt,Encodings.UTF8)
                  tlgt = tlgt.Replace("</h2>", rps)
                  'p_desc =  "<div id=""p_info"">" + tlgt + "<br/>" + "</div><br/>" +  p_desc + "<br/>" + p_artlisting
                  p_desc =  tlgt + "<br/>" + "<br/>" +  p_desc + "<br/>" + p_artlisting
                  
                Else
                  'p_desc = "<div id=""p_info"">" + luggGlobalBT + "</div><br/>" + p_desc + "<br/>" +p_artlisting
                  p_desc = luggGlobalBT + "<br/>" + p_desc + "<br/>" +p_artlisting
                End If
                
              ElseIf(AWS=2)Then //Artikel basierend
                if not (ozgew="") Then
                  p_welcome = ConvertEncoding(p_welcome,Encodings.UTF8)
                  tlgt = ConvertEncoding(tlgt,Encodings.UTF8)
                  tlgt = p_welcome
                  tlgt = tlgt.ReplaceAll("</h2>", rps)
                  p_desc =  tlgt + p_desc + "<br/>" + p_artlisting
                  
                Else
                  p_desc =  p_welcome  + "<br/>" + p_desc + "<br/>" + p_artlisting
                End If
                
              ElseIf(AWS=1) OR (AWS=0)Then //Eigener Text
                if not (ozgew="") Then
                  'p_desc =  "<div id=""p_info"">" + ArtThisText + "<br/>" + ozGew + " &euro;. <br/>" + "</div><br/>" +  p_desc + "<br/>" + p_artlisting
                  p_desc =   ArtThisText + "<br/>" + ozGew + " &euro;. <br/>" + "<br/>" +  p_desc + "<br/>" + p_artlisting
                  
                Else
                  'p_desc = "<div id=""p_info"">" + ArtThisText + "</div><br/>" + p_desc+ "<br/>" + p_artlisting
                  p_desc =  ArtThisText + "<br/>" + p_desc+ "<br/>" + p_artlisting
                End If
                
              Elseif AWS=-1 Then //Kein BT Gewählt
                p_desc = p_desc+ "<br/>" + p_artlisting
              End If
              
              
              
              //
              //
              // Replace $Artikelname$ with p_name
              p_desc = p_desc.ReplaceAll("$Artikelname$",p_name)
              p_desc = p_desc.ReplaceAll("$HEADArtikelname$","<h2>"+p_name+"</h2>")
              p_desc = p_desc.ReplaceAll("$Artikelnumber$",p_model)
              //Replace Lugg BT Passages
              p_desc = p_desc.ReplaceAll("$BT_Passage_1$",luggGBT(0))
              p_desc = p_desc.ReplaceAll("$BT_Passage_2$",luggGBT(1))
              p_desc = p_desc.ReplaceAll("$BT_Passage_3$",luggGBT(2))
              p_desc = p_desc.ReplaceAll("$BT_Passage_4$",luggGBT(3))
              p_desc = p_desc.ReplaceAll("$BT_Passage_5$",luggGBT(4))
              //#####
              p_desc = p_desc.ReplaceAll("$BT_Passage1$",luggGBT(0))
              p_desc = p_desc.ReplaceAll("$BT_Passage2$",luggGBT(1))
              p_desc = p_desc.ReplaceAll("$BT_Passage3$",luggGBT(2))
              p_desc = p_desc.ReplaceAll("$BT_Passage4$",luggGBT(3))
              p_desc = p_desc.ReplaceAll("$BT_Passage5$",luggGBT(4))
              
              
              p_desc = p_desc.ReplaceAll("$Artikelname$",p_name)
              p_desc = p_desc.ReplaceAll("$HEADArtikelname$","<h2>"+p_name+"</h2>")
              p_desc = p_desc.ReplaceAll("$Artikelnumber$",p_model)
              
              
              //LP Token
              While p_desc.Contains("%LP$")
                Dim ttx As String = p_desc.Between("$_","%LP$")
                Dim pLP As String = "$_"+ttx+"%LP$"
                Dim tix As Integer = val(ttx)
                Dim tLPD As Double = (tix / 100)
                
                
                p_desc = p_desc.ReplaceAll(pLP,Format(mProd.p_listprice*tLPD,"###,##0.00"))
              Wend
              //VK Token
              While p_desc.Contains("%VK$")
                Dim ttx As String = p_desc.Between("$_","%VK$")
                Dim pLP As String = "$_"+ttx+"%VK$"
                Dim tix As Integer = val(ttx)
                Dim tLPD As Double = (tix / 100)
                
                
                p_desc = p_desc.ReplaceAll(pLP,Format(mProd.p_outprice*tLPD,"###,##0.00"))
              Wend
              
              
              //p_desc anders aufbauen
              
              '"<!--attachments-->"<!--downloads-->""<!--details-->"
              
              
              p_specifications = p_specifications.TidyHTML()
              'If p_specifications.Between("<table","</table>").Len>0 Then
              'Dim tTable As String = p_specifications.Between("<table","</table>")
              'Dim ntable As String = GenerateTableFromString(tTable,mProd)
              'p_specifications = p_specifications.Replace(tTable,nTable)
              'End If
              supplData = supplData.TidyHTML()
              If supplData.Between("<table","</table>").Len>0 Then
                Dim tTable As String = supplData.Between("<table","</table>")
                Dim ntable As String = GenerateTableFromString(tTable,mProd)
                supplData = supplData.Replace(tTable,nTable)
              End If
              p_downloads = p_downloads.TidyHTML()
              p_downloads = p_downloads.ReplaceAll("Sorry,pdf","Sorry.pdf")
              
              
              'if p_name.contains("OSLO") Then
              'Dim oslo As Boolean
              'End If
              
              p_desc = p_desc.TidyHTML()
              
              
              
              
              
              
              
              
              //
              //ignore tables in description to prohibit automatic TAG replacement
              //
              'If p_desc.Between("<table","</table>").Len>0 Then
              'Dim tTable As String = p_desc.Between("<table","</table>")
              'Dim ntable As String = GenerateTableFromString(tTable,mProd)
              'p_desc = p_desc.Replace(tTable,nTable)
              'End If
              
              
              Dim exp_desc As String
              
              
              exp_desc = "<!--description-->" + p_desc + "<!--/description-->" +_
              "<!--details-->" + p_specifications + "<!--/details-->"+_
              "<!--attachments-->" + supplData + "<!--/attachments-->"+_
              "<!--downloads-->" + p_downloads + "<!--/downloads-->"
              
              
              exp_desc = exp_desc.replaceAll("&SM",";").replaceAll("&SEM",":")
              'p_desc = p_desc.TidyHTML()
              
              //sometimes Tidy deletes the nesseccary Description info
              'if not (p_desc.Contains("<!--description-->")) Then p_desc = "<!--description-->" + p_desc
              
              //
              //
              //
              // Sort Images and then join to one statement
              
              If pImages.Ubound>-1 Then
                pImages.Sort
                Dim pin,pnn As Integer
                Dim ptxs() As String
                pnn=pImages.Ubound
                for pin=0 to pnn
                  ptxs=pImages(pin).Split("=")
                  if pin+1<=ExpPicCount Then
                    
                    pImagesOut = pImagesOut + ptxs(1)
                    if pin<pnn Then pImagesOut = pImagesOut + FeldTrenner
                  Else
                    ErrorList.AddRow(" Bildüberlauf - >"+ptxs(1) +"< ("+str(pin+1)+"/"+str(pnn)+") Erlaubt: "+str(ExpPicCount))
                  End If
                next
              End If
              'quit
              'MsgBox(p_downloads + EndOfLine + EndOfLine + p_movies)
              
              ExportList.Append "XTSOL" + FeldTrenner + action + FeldTrenner + p_model + FeldTrenner + p_stock + FeldTrenner +_
              "0" + FeldTrenner + p_shipping + FeldTrenner + p_tpl.ReplaceAll(EndOfLine,"") + FeldTrenner + IIF(ExpName.Len>0,ExpName,p_manufacturer) + FeldTrenner +_
              "0" + FeldTrenner + p_priceNoTax + FeldTrenner + p_priceNoTax1 + FeldTrenner + p_priceNoTax2 +_
              FeldTrenner + p_minPriceDe + FeldTrenner + "1" + FeldTrenner + "1" + FeldTrenner + "0.00" +_
              FeldTrenner + p_ean + FeldTrenner + ExpDiscount + FeldTrenner + p_opttpl.ReplaceAll(EndOfLine,"") + FeldTrenner + p_vpe + FeldTrenner +_
              p_vpe_status + FeldTrenner + p_vpe_value + FeldTrenner + p_name + FeldTrenner + exp_desc + FeldTrenner +_
              p_shortdesc + FeldTrenner + p_meta_title + FeldTrenner + p_meta_desc + FeldTrenner +_
              p_meta_key + FeldTrenner + p_keywords + FeldTrenner + p_url + FeldTrenner +_
              p_cat1  + FeldTrenner + p_cat2 + FeldTrenner + p_cat3 + FeldTrenner + p_cat4 + FeldTrenner + p_cat5 + FeldTrenner + p_google + FeldTrenner +_
              p_EnergyClass + FeldTrenner + p_EnergyClassPict + FeldTrenner + p_EnergyClassText + Feldtrenner +_
              p_movies + Feldtrenner + pImagesOut + "$EOL$"'EndOfLine.Windows' 'EndOfLine
              
              'ExpField.Text = ExpField.Text +   exp 'EndOfLine + "#######" + endofline +
              
              'ExportList(ExportList.Ubound) = ExportList(ExportList.Ubound).replaceAll("&SM",";").replaceAll("&SEM",":")
              
              
            End If
            
            
          Else
            
            ErrorList.AddRow("[!!!] Datei (" + str(ii) + ") nicht gefunden! - " + oof.name)
            
          End If
        End If
        
      End If
      
      app.DoEvents
    Next
    
    
    WalkerScroll.value = n
    WalkerScroll.Refresh()
    
    WalkerLbl.Text = "Fertig! " + str(n) + " Artikel zum Export aufbereitet."
    
    Dim exi,exn As Integer
    exn = ExportList.Ubound
    If exn>-1 Then
      For exi=0 to exn
        #pragma BackgroundTasks False
        exp = exp +  ExportList(exi)
        #pragma BackgroundTasks True
      Next
    End If
    
    exp = exp.ReplaceAll(EndOfLine.Windows,"")
    exp = exp.ReplaceAll(EndOfLine.Macintosh,"")
    exp = exp.ReplaceAll(EndOfLine.UNIX,"")
    exp = exp.ReplaceAll(EndOfLine.Windows+EndOfLine.Windows,"")
    exp = exp.ReplaceAll(EndOfLine.Macintosh+EndOfLine.Macintosh,"")
    exp = exp.ReplaceAll(EndOfLine.UNIX+EndOfLine.UNIX,"")
    
    exp = exp.ReplaceAll("$EOL$",EndOfLine.Windows)
    exp = exp.ReplaceAll("...","")
    
    ExpField.Text = exp
    
    TBB_Save.Visible = True
    TBB_Save.Enabled = True
    TBB_Save.Refresh()
    TBB_Save.PerformAction()
    'WalkerScroll.Visible = False
    
  End If
  
  
  App.ExportTask = False
  
  
End Sub


' ###############
' DEPENDING FUNCTIONS
'

Function ReplaceCTRLChars(z As String) As String
  z = z.ReplaceAll("&SEM",":")
  z = z.ReplaceAll("&SM",";")
  z = z.ReplaceAll("&EOL","")
  z = z.ReplaceAll("'","""")
  
  return z
End Function


Sub UnWrappListData(LB As ListBox, k As String)
  LB.DeleteAllRows()
  
  'k = DecodeHTML(k)
  k = k.replaceAll("::::",":: ::")
  'k = k.replaceAll("&SM",";")
  'k = k.replaceAll("&SEM",":")
  
  Dim techData() As String = k.Split("§-§")
  Dim kt() As String
  Dim ti,tn As Integer
  Dim tk As String
  tn = techData.Ubound
  if tn>-1 Then
    For ti=0 to tn
      tk = techData(ti)
      If tk.StartsWith("PUM::") Then
        
        kt = tk.Split("::")
        if kt.Ubound >= 1 Then
          LB.AddRow(kt(1).ReplaceAll("&SEM",":").replaceAll("&SM",";"))
        End If
        if kt.Ubound = 2 Then
          LB.Cell(LB.LastIndex,1) = "..."
          LB.CellTag(LB.LastIndex,1) = "PUM::" + kt(2)
        End If
        if kt.Ubound = 3 Then
          LB.Cell(LB.LastIndex,1) = kt(2)
          LB.CellTag(LB.LastIndex,1) = "PUM::" + kt(2) + "::" + kt(3)
        End If
      ElseIf tk.StartsWith("EF::") Then
        'MsgBox(k)
        kt = tk.Split("::")
        if kt.Ubound >= 1 Then
          LB.AddRow(kt(1).ReplaceAll("&SEM",":").replaceAll("&SM",";"))
        End If
        if kt.Ubound = 2 Then
          LB.Cell(LB.LastIndex,1) = kt(2)
          LB.CellTag(LB.LastIndex,1) = "EF::" + kt(2)
        End If
      ElseIf tk.StartsWith("HEAD::") Then
        'MsgBox(k)
        kt = tk.Split("::")
        if kt.Ubound >= 1 Then
          LB.AddRow(kt(1).ReplaceAll("&SEM",":").replaceAll("&SM",";"))
          LB.CellTag(LB.LastIndex,0) = "HEAD::" + kt(1)
        End If
        if kt.Ubound = 2 Then
          LB.Cell(LB.LastIndex,1) = kt(2)
          LB.CellTag(LB.LastIndex,0) = "HEAD::" + kt(1)
          LB.CellTag(LB.LastIndex,1) = "HEAD::" + kt(2)
        End If
      End If
    Next
  End If
End Sub


Function prod_generateEnergyTechData(techData As String) As String
  '
  ' Data cue in Dict ->  ID, TYPE, NAME, SELECTED VALUE, opt VALUES
  '                     .key   0    1            2           3
  '
  
  '
  'PUM::HohenverstellbareAusgleichsfüße::Ja::Ja][Nein][nichtvorhanden][ @[[0000121]];
  ' –          ––––––––––                ––    ––––––––––––––––––––---   –––––––––
  ' |              |                      |              |                  |
  'TYPE           NAME             SELECTED VALUE     VALUES                ID
  '
  
  
  '
  'EF::Höhe der Innenwanne::keine Wertevorhanden@[[0000117]];
  ' –       ––––––––––              ––            –––––––––
  ' |           |                   |                 |
  'TYPE        NAME          SELECTED VALUE           ID
  '
  
  '
  ' ID -> @[[0000117]]
  '
  ' Array -> Value_0][Value_1][Value_2][
  '          Value_0][Value_1][Value_2
  '
  '
  
  DIm encTech,outData As String
  
  encTech = techData.ReplaceAll(":::","::")
  
  Dim tData() As String = encTech.Split("§-§")
  DIm ti,tn As Integer
  Dim tLine, lastID, nextID, txCell As String
  Dim tCells() As String
  Dim pv(6) As String
  Dim li,ln As Integer
  Dim xID As String
  
  //Get the template lines
  //sort the lines depending on the arrangement of the template
  //then get the changed parameters of Pupopboxes, etc.
  // -> save the file
  
  //First: clean the tData >> trim empty cells
  tn = tData.Ubound
  if tn>-1 Then
    For ti=tn to 0
      if tData(ti).Len=0 or tData(ti)=" " Then
        tData.Remove(ti)
      End If
    Next
  End If
  //Create a tData Dict
  //templateDict already exists with array values (pv[])
  Dim tDict As New Dictionary // The data dict
  Dim toDict As New Dictionary // The dictionary we use to save the data
  Dim tIDCounter As Integer = 0
  tn = tData.Ubound
  If tn>-1 Then
    
    Dim tID,cID As String
    For ti=0 to tn
      
      '#if DebugBuild
      'if (mProd.ArtNr.Contains("Gra-962820011")) and(ti=70) Then
      '
      'break
      'End If
      '
      '#endif
      
      DIm tpv(6) As String
      
      //get the reference ID
      tID = RegEx_ExtractParam(tData(ti),"[@][[][[](.*)[]][]]").Replace(maskName+".","").Replace("@[[]]","")
      //cover up lines without ID's like optional supply products
      tID = RegEx_ExtractParam(tID,"(?mi-s)(?:[0-9]*)",true) 'ReplaceAllRegExB("(?:[a-z])","").Replace(".","")//strip all masknames from IDs
      if tID.len=0 or tID="" or tID = " " Then
        tID = "t_"+str(tIDCounter)
        tIDCounter = tIDCounter + 1
      End If
      
      tLine = tData(ti)
      tLine = tLine.ReplaceAll("@[["+maskName+"."+tID+"]]","")
      tLine = tLine.ReplaceAll("@[["+maskName+".]]","")
      tLine = tLine.ReplaceAll(tID,"").ReplaceAll("@[[]]","")
      tCells = tLine.Split("::")
      ln = tCells.Ubound
      if ln>=2 Then
        //now get the fieldType
        //DecodeHTML
        tpv(0) = tCells(0) //Fieldtype like EF / PUM / HEAD
        tpv(1) = tCells(1).ReplaceAll("&SEM",":").ReplaceAll("&SM",";") 'FieldName like Produkttyp
        tpv(2) = tCells(2).ReplaceAll("&SEM",":").ReplaceAll("&SM",";") 'FieldValue like Bain Marie
        if tCells.Ubound>=3  Then tpv(3) = tCells(3) //PUM -> PopUpMenu
        
        tpv(6) = tID
        
        tDict.Value(tID) = tpv
        
      End If
    Next
    
    //Now cycle through idDict and sort the values and assing new parameters
    //if there's a new fallback param for a value where the tDict param has no value, assign it
    Dim ci,cn As Integer
    
    cn = idDict.count -1
    if cn>-1 then
      For ci=0 to cn
        
        '#if DebugBuild
        'if (mProd.ArtNr.Contains("Gra-962820011")) and(ci=71) Then
        '
        'break
        'End If
        '
        '#endif
        
        Dim cPV(6) As String //shall be 6
        
        //get the keys, then check if tDict has the key
        //then add the values to the toDict
        cID = str(idDict.Key(ci)).Replace(maskName+".","").Replace("@[[]]","")
        cPV = idDict.value(cID)
        if cPV.Ubound>=2 Then
          if cID.StartsWith("t_") and tdict.haskey(cID) Then
            toDict.value(cID) = tDict.Value(cID)
            continue for ci
          elseif cID.StartsWith("t_") and (not(tdict.HasKey(cID))) Then
            toDict.value(cID) = idDict.Value(cID)
            continue for ci
          End If
          If tDict.hasKey(cID) Then //does the file has the key, then refreh the params
            Dim tPV(6) As String
            tPV = tDict.Value(cID)
            'if tPV(3).Len>0 Then
            tPV(0) = cPV(0)
            tPV(3) = cPV(3) //assing the new values
            'End If
            toDict.value(cID) = tPV
          Else //add the new line to the File
            toDict.Value(cID) = cPV
          End If
        End If
      Next
    End If
    
    //now generate the new TECHDATA SELECTOR content
    Redim tData(-1)
    Dim tv(6) As String
    Dim tvID As String
    tn = toDict.Count -1
    if tn>-1 Then 
      For ti=0 to tn
        
        '#if DebugBuild
        'if (mProd.ArtNr.Contains("Gra-960840281")) and(ti=47) Then
        '
        'break
        'End If
        '
        '#endif
        
        tLine = ""
        redim tv(6)
        tvID = toDict.Key(ti)
        tv = toDict.Value(tvID)
        if tvID.StartsWith("t_") Then 
          tvID = ""
        End If
        if tv(0) = "" Then tv(0) = " "
        if tv(1) = "" Then tv(1) = " "
        if tv(2) = "" Then tv(2) = " "
        Dim tv2Enc,tv3Enc As String
        tv2Enc = EncodeHTML(tv(2))
        tv3Enc = EncodeHTML(tv(3))
        if (tv(3).contains(tv(2)) or tv(2).Contains(tv(3)) or _
          tv3Enc.contains(tv2Enc) or tv2Enc.Contains(tv3Enc)) and tv(2).contains("][") Then //clean misused paramArray and insert blank space, as a workaround for triplesplit of :::: which results in 0:: 1:: 2::
          tv(2) = " "
        End If
        if tv(3).Len>0 Then
          //PUM::HohenverstellbareAusgleichsfüße::Ja::Ja][Nein][nichtvorhanden][ @[[0000121]]
          tLine = tv(0) + "::" + tv(1) + "::" + tv(2) + "::" + tv(3) + "@[["+maskName+"."+tvID+"]]"
        Else
          //EF::Höhe der Innenwanne::keine Wertevorhanden@[[0000117]]
          tLine = tv(0) + "::" + tv(1) + "::" + tv(2) + "@[["+maskName+"."+tvID+"]]"
        End If
        //EncodeHTML
        tData.Append tLine
      Next
    End If
    
    if tData.Ubound>-1 Then
      outData = Join(tData,"§-§")
      
      'Dim b As Boolean = mProd.ChangeSector("TECHDATA",outData)
      
      return outData //energyclassText
    End If
    
  End If
  return outdata
End Function


Sub generateTemplateDict(maskDir As FolderItem)
  Dim xf As FolderItem = maskDir
  if xf<>nil and xf.Exists Then
    
    idDict = New Dictionary
    Redim templateLines(-1)
    
    Dim tFieldID As String
    Dim tIDCounter As Integer = 0
    Dim xt As String = OpenFile(xf)
    Dim t(),k,kt(),lastID,nextID As String
    xt = xt.ReplaceAll(REALbasic.EndOfLine,"")
    t = xt.Split(";")
    
    //collect the generic IDs with their values
    if t.Ubound > -1 Then
      Dim i,n As Integer
      n = t.Ubound
      
      //get the maskName separate
      FOr i=0 to n
        k = t(i)
        if k.StartsWith("NAME::") Then
          k = k.Replace("NAME::","")
          maskName = k
          Exit For i
        End If
      Next
      
      if maskName.Len=0 Then
        maskName = xf.NameWithoutExtension_MTC
      End If
      
      for i=0 to n
        Dim pv(6) As String
        k = t(i)
        if k.len>0 Then
          
          
          tFieldID = RegEx_ExtractParam(k,"[@][[][[](.*)[]][]]")
          
          if i<n Then nextID = RegEx_ExtractParam(t(i+1),"[@][[][[](.*)[]][]]")
          k = k.Replace(tFieldID,"").Replace("@[[]]","")
          
          kt = k.Split("::")
          if kt.Ubound >= 1 Then
            'if tFieldID.len>0 Then 
            'redim pv(1)
            
            if (kt(0) = "NAME") or (kt(0) = "DESC") Then continue for i
            
            //if i line without ID generate a temporary one
            if tFieldID.len=0 or tFieldID="" or tFieldID = " " Then
              tFieldID = "t_"+str(tIDCounter)
              tIDCounter = tIDCounter + 1
            End If
            //DecodeHTML
            pv(0) = kt(0) //Fieldtype like EF / PUM / HEAD
            pv(1) = kt(1).ReplaceAll("&SEM",":").ReplaceAll("&SM",";") 'FieldName like Produkttyp
            pv(2) = kt(2).ReplaceAll("&SEM",":").ReplaceAll("&SM",";") 'FieldValue like Bain Marie
            if kt.Ubound>=3 Then pv(3) = kt(3) //PUM -> PupUpMenu
            '
            ' add indices for upper and under xID to perform insert line
            ' id pv(5) is top xIDs
            if lastID.Len>0 Then pv(5) = lastID
            if nextID.Len>0 Then pv(6) = nextID
            
            idDict.Value(str(tFieldID)) = pv' kt(1).ReplaceAll("&SEM",":").ReplaceAll("&SM",";")
            
            templateLines.Append k
            
            'End If
          End If
          
          
          
          
          lastId = tFieldID
          
        End If
      Next
    End If
    
    
  End If
End Sub

Function GenerateTableFromString(TechData As String, mProd As pProduct) As String
  
  TechData = TechData
  TechData = TechData.ReplaceAll(app.gDelimitter,"")
  
  Dim outData As String
  
  'outData = "<style type=""text/css"">.tooltip {cursor: help;color: rgb(66,110,240);font-weight: bold;text-decoration: underline;}.p_desc-table {font-family:"+_
  '"sans-serif;-webkit-font-smoothing: antialiased;font-size: 12px;width: 700px;overflow: auto;display: block; border-collapse: collapse;border: 1px solid #252525;}.p_desc-table th {display: table-cell;"+_
  '"background-color: rgb(215,225,245);text-align: left;font-weight: normal;color: rgb(70, 70, 70);padding: 7px 10px; border: 1px solid #252525;vertical-align: middle;}.p_desc-table td {"+_
  '"display: table-cell;padding: 7px 10px;text-align: left;vertical-align: middle;"+_
  '"color: rgb(70, 70, 70); border: 1px solid black;}.p_desc-table th span.tooltip{color: rgb(66,110,240);}.p_desc-table th.heading{font-weight: bold;font-size: 100%;background-color: rgb(135,155,185);color:white;}"+_
  '"p_desc-table thead{text-align:left;}</style>"
  
  's = s +"<table border="""+TableBorderWidth+""" cellpadding=""6"" cellspacing=""0"" width="""+TableWidth+""" style=""border:1px solid "+TableBorderColor+";""><tbody>"
  
  TechData = TechData.ReplaceAllRegEx("(<tr[^<>]+>)","<tr>")
  'TechData = TechData.ReplaceAllRegEx("(<table[^<>]+>)","<table class=""p_desc-table"">")
  Dim tss() As String = TechData.Split("<tr>")
  Dim ti,tn As Integer
  tn = tss.Ubound
  
  if tn>-1 Then 
    
    Dim tCell_0,tCell_1 As String
    Dim tCell_0Tag, tCell_1Tag As String
    
    Dim at,bt As Integer
    Dim tTokenOccur As Integer
    Dim ht,tToken As String
    
    TagDataLB.ColumnsortDirection(0)=ListBox.SortDescending
    TagDataLB.SortedColumn=0   //first column is the sort column
    TagDataLB.Sort
    
    bt = TagDataLB.LastIndex
    
    for ti=0 to tn
      
      tCell_0 = ""
      
      tCell_0Tag = ""
      
      if tss(ti).Contains("</tr>") Then
        tCell_0 = "<tr>" + tss(ti)
        if ti Mod 2 = 0 then
          tCell_0 = "<tr bgcolor=""#D8EBF4"">" + tss(ti) 
        Else
          tCell_0 = "<tr>" + tss(ti)
        End If
      ELseif (tss(ti) =">") Or (tss(ti) ="> ") Or (tss(ti) =" >") Or (tss(ti) =" > ") Then
        continue
      ELse
        tCell_0 = tss(ti)
      End If
      
      tCell_0Tag = tCell_0
      
      For at=0 to bt
        
        tToken = TagDataLB.Cell(at,0)
        ht = TagDataLB.Cell(at,1)
        ht = ht.ReplaceAll("&EOL","&#13;")
        
        if not (tCell_0="") or (tCell_0=" ") Then
          if (tCell_0.contains(tToken)) Then
            tCell_0Tag = tCell_0Tag.ReplaceAllOutsideXTag(tToken,"<span class="+Quote+"tooltip"+Quote+" title="+Quote+ht+Quote+">" + tToken + "</span>","span")
          End If
        End If
        
      next
      //---
      
      outData = outData + tCell_0Tag
      
      
    Next
    
    
  End If
  
  
  While outData.Contains("%LP$")
    Dim ttx As String = outData.Between("$_","%LP$")
    Dim pLP As String = "$_"+ttx+"%LP$"
    Dim tix As Integer = val(ttx)
    Dim tLPD As Double = (tix / 100)
    
    Dim zgV As String
    zgV = str(mProd.p_outprice)
    
    outData = outData.ReplaceAll(pLP,Format(val(zgV )*tLPD,"###,##0.00"))
  Wend
  outData = outData.ReplaceAll("$LP$",Format(mProd.p_listprice,"###,##0.00"))
  
  outData = EncodeHTML(outData)
  
  outData = outData.replaceAll("&SM",";")
  outData = outData.replaceAll("&SEM",":")
  
  return outData
End Function

Function GenerateListTablePrev(LB As ListBox, mProd As pProduct, ignoreColorCodes As Boolean = False) As String
  
  
  Dim s As String
  Dim nthColor As String = "#D8EBF4"
  Dim headColor As String = "#EFF5F8"
  
  Dim i,n As Integer
  n = LB.LastIndex
  s = "<style type=""text/css"">.tooltip {cursor: help;color: rgb(66,110,240);font-weight: bold;text-decoration: underline;}"+_
  "</style>"
  
  if not ignoreColorCodes Then
    s = s +"<table class=""p_desc-table"" style=""width:90%;max-width:95%;border-collapse: collapse; font-family:sans-serif;-webkit-font-smoothing: antialiased;""><tbody>"
  Else
    s = s + "<table><tbody>"
  End If
  Dim tCell_0,tCell_1 As String
  Dim tCell_0Tag, tCell_1Tag As String
  
  Dim a,bx As Integer
  Dim ht,tToken As String
  
  TagDataLB.ColumnsortDirection(0)=ListBox.SortDescending
  TagDataLB.SortedColumn=0   //first column is the sort column
  TagDataLB.Sort
  
  bx = TagDataLB.LastIndex
  
  'For a=0 to bx
  '
  'tToken = TagDataLB.Cell(a,0)
  'ht = TagDataLB.Cell(a,1)
  'ht = ht.ReplaceAll("&EOL","&#13;")
  's = s.ReplaceAllOutsideXTag(tToken,"<span class="+Quote+"tooltip"+Quote+" title="+Quote+ht+Quote+">" + tToken + "</span>","span")
  '
  'next
  Dim tdStyleLeft,tdStyleLeftA,tdStyleLeftB,tdStyleRight,tdStyleRightA,tdStyleRightB As String
  
  tdStyleLeftA = """border-bottom:1pt solid #DDDDDD;border-right:1pt solid #AAAAAA;border-top:1pt solid #AAAAAA;border-left:1pt solid #AAAAAA;font-size:1em;font-weight:300;padding-left:5px;padding-right:5px;padding-top:8px;padding-bottom:5px;"""
  tdStyleLeftB = """border-bottom:1pt solid #252525;border-right:1pt solid #AAAAAA;border-top:1pt solid #AAAAAA;border-left:1pt solid #AAAAAA;font-size:1em;font-weight:300;padding-left:5px;padding-right:5px;padding-top:8px;padding-bottom:5px;"""
  
  tdStyleRightA = """border-bottom:1pt solid #DDDDDD;border-right:1pt solid #AAAAAA;border-top:1pt solid #AAAAAA;font-size:1em;padding-left:5px;padding-top:8px;padding-bottom:5px;padding-right:5px;"""
  tdStyleRightB = """border-bottom:1pt solid #252525;border-right:1pt solid #AAAAAA;border-top:1pt solid #AAAAAA;font-size:1em;padding-left:5px;padding-top:8px;padding-bottom:5px;padding-right:5px;"""
  
  Dim xd As Integer = 0
  
  if n > -1 Then
    for i=0 to n
      
      tCell_0 = ""
      tCell_1 = ""
      tCell_0Tag = ""
      tCell_1Tag = ""
      
      tCell_0 = LB.Cell(i,0).ReplaceAllRegEx("([@][[][[].*[]][]])","",False).replaceAll("]§","").replaceAll("§[","")
      tCell_1 = LB.Cell(i,1).ReplaceAllRegEx("([@][[][[].*[]][]])","",False).replaceAll("]§","").replaceAll("§[","")
      
      tCell_0Tag = tCell_0
      tCell_1Tag = tCell_1
      
      
      
      For a=0 to bx
        
        tToken = TagDataLB.Cell(a,0)
        
        'if tCell_0Tag.Contains("uml;") or tCell_0Tag.Contains("&szlig;") Then tToken = EncodeHTML(tToken)
        
        ht = TagDataLB.Cell(a,1)
        ht = ht.ReplaceAll("&EOL","&#13;")
        if not (tCell_0="") or (tCell_0=" ") Then
          if (tCell_0.contains(tToken)) Then
            tCell_0Tag = tCell_0Tag.ReplaceAllOutsideXTag(tToken,"<span class="+Quote+"tooltip"+Quote+" title="+Quote+ht+Quote+">" + tToken + "</span>","span")
            'Exit For
          End If
        End If
        if not (tCell_1="") or (tCell_1=" ") Then
          If (tCell_1.contains(tToken)) Then
            tCell_1Tag = tCell_1Tag.ReplaceAllOutsideXTag(tToken,"<span class="+Quote+"tooltip"+Quote+" title="+Quote+ht+Quote+">" + tToken + "</span>","span")
            'Exit For
          End If
        End If
      next
      
      If LB.CellTag(i,0).StringValue.StartsWith("HEAD") Or LB.CellTag(i,1).StringValue.StartsWith("HEAD") Then
        //wenn 0 dann keine extrazeile, wenn i>0 dann prefix zeile
        if not ignoreColorCodes Then
          if(not (i=0 or i=n))Then
            s = s + "<tr bgcolor=""#FFFFFF""><td style=""border-left:1pt solid #AAAAAA;"">&nbsp;</td><td style=""border-right:1pt solid #AAAAAA;"">&nbsp;</td></tr>"
          End If
          s = s + "<tr bgcolor="""+headColor+"""><td style=""border-top:1pt solid #252525;border-bottom:1pt solid #DDDDDD;border-left:1pt solid #AAAAAA;font-size:1.1em;font-weight:300;padding-top:25px;padding-bottom:10px;padding-left:5px;padding-right:5px;"">" + tCell_0Tag + "&nbsp;</td><td style=""border-top:1pt solid #252525;border-bottom:1pt solid #DDDDDD;border-right:1pt solid #AAAAAA;font-size:1.1em;font-weight:300;padding-left:5px;padding-top:25px;padding-bottom:10px;padding-right:5px;"">" + tCell_1Tag + "</td></tr>" 'th class=""heading""
        Else
          s = s + "<tr><td>" + tCell_0Tag + "</td></tr><tr><td>" + tCell_1Tag + "</td></tr>"
        End If
        xd = 1
      Else
        if i=n Then
          tdStyleLeft = tdStyleLeftB
          tdStyleRight = tdStyleRightB
        Else
          tdStyleLeft = tdStyleLeftA
          tdStyleRight = tdStyleRightA
        End If
        if not ignoreColorCodes Then
          if xd Mod 2 = 0 then
            s = s + "<tr bgcolor="""+nthColor+"""><td style="+tdStyleLeft+">" + tCell_0Tag + "&nbsp;</td><td style="+tdStyleRight+">" + tCell_1Tag + "</td></tr>"
            xd = xd + 1
          Else
            s = s + "<tr bgcolor=""#FFFFFF""><td style="+tdStyleLeft+">" + tCell_0Tag + "&nbsp;</td><td style="+tdStyleRight+">" + tCell_1Tag + "</td></tr>"
            xd = xd + 1
          End If
        Else
          s = s + "<tr><td>" + tCell_0Tag + "</td></tr><tr><td>" + tCell_1Tag + "</td></tr>"
          xd = xd + 1
        End If
      End If
    next
  End If
  '<span class="tooltip" title="Während der Kühlung setzt sich Feuchtigkeit am Verdampfer an und gefriert, während der Abtauung wird das Eis flüssig und wird in einer speziellen Auffangschale verdunstet">Tauwasserverdunstung</span>
  
  
  
  
  s = s + "</tbody> </table>"
  
  While s.Contains("%LP$")
    Dim ttx As String = s.Between("$_","%LP$")
    Dim pLP As String = "$_"+ttx+"%LP$"
    Dim tix As Integer = val(ttx)
    Dim tLPD As Double = (tix / 100)
    
    Dim zgV As String
    
    zgV = str(mProd.p_outprice)
    
    
    s = s.ReplaceAll(pLP,Format(val(zgV )*tLPD,"###,##0.00"))
  Wend
  s = s.ReplaceAll("$LP$",Format(mProd.p_listprice,"###,##0.00"))
  
  s = EncodeHTML(s)
  
  s = s.replaceAll("&SM",";")
  s = s.replaceAll("&SEM",":")
  
  return s
End Function
