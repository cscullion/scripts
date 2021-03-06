#!/usr/bin/python

import urllib
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

#params = urllib.urlencode({'GUID': 'f34e4b2a-44b9-409f-aa29-170038188517', \
#                           'ExtInterfaceID': '0', \
#                           'EngineID': '2', \
#                           'OfferID': '9'})
params = '''<?xml version="1.0" encoding="utf-8"?>
      <ei>
        <m_eiguid>f34e4b2a-44b9-409f-aa29-170038188517</m_eiguid>
        <m_extInterfaceID>0</m_extInterfaceID>
      </ei>
      <os>
        <m_offers>
          <OfferDefinition>
            <m_offerID>101</m_offerID>
            <m_extOfferID>990002</m_extOfferID>
            <m_filename></m_filename>
            <m_offerXML>
                <Offer>
                  <Header>
                    <IncentiveID DataType="Int64">1</IncentiveID>
                    <EngineID DataType="Int32">2</EngineID>
                    <IsTemplate DataType="Boolean">False</IsTemplate>
                    <FromTemplate DataType="Boolean">False</FromTemplate>
                    <IncentiveName DataType="String">ckstest 1</IncentiveName>
                    <Description DataType="String"></Description>
                    <PromoClassID DataType="Int32">1</PromoClassID>
                    <Priority DataType="Int32">2</Priority>
                    <StartDate DataType="DateTime">7/23/2018 12:00:00 AM</StartDate>
                    <EndDate DataType="DateTime">7/23/2019 12:00:00 AM</EndDate>
                    <EveryDOW DataType="Int32">1</EveryDOW>
                    <EligibilityStartDate DataType="DateTime">7/23/2018 12:00:00 AM</EligibilityStartDate>
                    <EligibilityEndDate DataType="DateTime">7/23/2018 12:00:00 AM</EligibilityEndDate>
                    <TestingStartDate DataType="DateTime">7/23/2018 12:00:00 AM</TestingStartDate>
                    <TestingEndDate DataType="DateTime">7/23/2019 12:00:00 AM</TestingEndDate>
                    <P1DistQtyLimit DataType="Int32">1</P1DistQtyLimit>
                    <P1DistTimeType DataType="Int32">2</P1DistTimeType>
                    <P1DistPeriod DataType="Int32">1</P1DistPeriod>
                    <P3DistQtyLimit DataType="Int32">1</P3DistQtyLimit>
                    <P3DistTimeType DataType="Int32">2</P3DistTimeType>
                    <P3DistPeriod DataType="Int32">1</P3DistPeriod>
                    <EnableRedeemRpt DataType="Boolean">False</EnableRedeemRpt>
                    <CreatedDate DataType="DateTime">7/24/2018 8:19:52 AM</CreatedDate>
                    <LastUpdate DataType="DateTime">7/24/2018 8:26:09 AM</LastUpdate>
                    <Deleted DataType="Int32">0</Deleted>
                    <StatusFlag DataType="Int32">0</StatusFlag>
                    <UpdateLevel DataType="Int32">2</UpdateLevel>
                    <CRMEngineID DataType="Int32">0</CRMEngineID>
                    <CRMEngineUpdateLevel DataType="Int32">0</CRMEngineUpdateLevel>
                    <CPEOADeployStatus DataType="Int32">1</CPEOADeployStatus>
                    <CPEOARptDate DataType="DateTime">7/24/2018 8:26:45 AM</CPEOARptDate>
                    <CPEOADeploySuccessDate DataType="DateTime">7/24/2018 8:26:45 AM</CPEOADeploySuccessDate>
                    <DisabledOnCFW DataType="Boolean">True</DisabledOnCFW>
                    <AllowOptOut DataType="Boolean">False</AllowOptOut>
                    <EmployeesOnly DataType="Boolean">False</EmployeesOnly>
                    <EmployeesExcluded DataType="Boolean">False</EmployeesExcluded>
                    <DeferCalcToEOS DataType="Boolean">False</DeferCalcToEOS>
                    <CreatedByAdminID DataType="Int32">1</CreatedByAdminID>
                    <LastUpdatedByAdminID DataType="Int32">1</LastUpdatedByAdminID>
                    <SendIssuance DataType="Int32">0</SendIssuance>
                    <EveryTOD DataType="Int32">1</EveryTOD>
                    <ManufacturerCoupon DataType="Int32">0</ManufacturerCoupon>
                    <VendorCouponCode DataType="String"></VendorCouponCode>
                    <TierLevels DataType="Byte">1</TierLevels>
                    <MutuallyExclusive DataType="Boolean">False</MutuallyExclusive>
                    <EnableImpressRpt DataType="Boolean">False</EnableImpressRpt>
                    <EngineSubTypeID DataType="Int32">0</EngineSubTypeID>
                    <AutoTransferable DataType="Boolean">True</AutoTransferable>
                    <RestrictedRedemption DataType="Boolean">False</RestrictedRedemption>
                    <DisplayOnWebKiosk DataType="Boolean">False</DisplayOnWebKiosk>
                    <UseLegacyWebKiosk DataType="Boolean">False</UseLegacyWebKiosk>
                  </Header>
                  <Conditions>
                    <Customer>
                      <IncentiveCustomerID DataType="Int32">1</IncentiveCustomerID>
                      <RewardOptionID DataType="Int64">1</RewardOptionID>
                      <CustomerGroupID DataType="Int32">6</CustomerGroupID>
                      <ExcludedUsers DataType="Boolean">false</ExcludedUsers>
                      <Deleted DataType="Boolean">false</Deleted>
                      <LastUpdate DataType="DateTime">7/24/2018 8:21:54 AM</LastUpdate>
                      <ConditionNumber DataType="String">0</ConditionNumber>
                      <HHEnable DataType="Boolean">false</HHEnable>
                      <RequiredFromTemplate DataType="Boolean">false</RequiredFromTemplate>
                    </Customer>
                    <Product>
                      <IncentiveProductGroupID DataType="Int32">1</IncentiveProductGroupID>
                      <RewardOptionID DataType="Int64">1</RewardOptionID>
                      <ProductGroupID DataType="Int32">4</ProductGroupID>
                      <QtyForIncentive DataType="Decimal">5.000000</QtyForIncentive>
                      <QtyUnitType DataType="Int32">1</QtyUnitType>
                      <AccumMin DataType="Decimal">0.000</AccumMin>
                      <AccumLimit DataType="Decimal">0.000</AccumLimit>
                      <AccumPeriod DataType="Int32">0</AccumPeriod>
                      <ExcludedProducts DataType="Boolean">false</ExcludedProducts>
                      <Deleted DataType="Boolean">false</Deleted>
                      <LastUpdate DataType="DateTime">7/24/2018 8:23:24 AM</LastUpdate>
                      <ConditionNumber DataType="String">0</ConditionNumber>
                      <ProductComboID DataType="Int32">0</ProductComboID>
                      <RequiredFromTemplate DataType="Boolean">false</RequiredFromTemplate>
                      <Disqualifier DataType="Boolean">false</Disqualifier>
                      <Rounding DataType="Boolean">false</Rounding>
                      <MinPurchAmt DataType="Decimal">0.000000</MinPurchAmt>
                      <UniqueProduct DataType="Boolean">false</UniqueProduct>
                      <Tiers>
                        <Tier>
                          <PKID DataType="Int64">1</PKID>
                          <IncentiveProductGroupID DataType="Int32">1</IncentiveProductGroupID>
                          <RewardOptionID DataType="Int64">1</RewardOptionID>
                          <TierLevel DataType="Byte">1</TierLevel>
                          <Quantity DataType="Decimal">5.000000</Quantity>
                        </Tier>
                      </Tiers>
                    </Product>
                  </Conditions>
                  <Notifications />
                  <Rewards>
                    <Discount>
                      <DiscountID DataType="Int32">1</DiscountID>
                      <Name DataType="String"></Name>
                      <DiscountTypeID DataType="Int32">3</DiscountTypeID>
                      <ReceiptDescription DataType="String">offer 1 .05 off</ReceiptDescription>
                      <SpecifyBarcode DataType="Boolean">false</SpecifyBarcode>
                      <DiscountBarcode DataType="String"></DiscountBarcode>
                      <VoidBarcode DataType="String"></VoidBarcode>
                      <DiscountedProductGroupID DataType="Int32">1</DiscountedProductGroupID>
                      <ExcludedProductGroupID DataType="Int32">0</ExcludedProductGroupID>
                      <BestDeal DataType="Boolean">false</BestDeal>
                      <AllowNegative DataType="Boolean">false</AllowNegative>
                      <ComputeDiscount DataType="Boolean">true</ComputeDiscount>
                      <DiscountAmount DataType="Decimal">0.050000</DiscountAmount>
                      <AmountTypeID DataType="Int32">1</AmountTypeID>
                      <L1Cap DataType="Decimal">0.000000</L1Cap>
                      <L2DiscountAmt DataType="Decimal">0.000000</L2DiscountAmt>
                      <L2AmountTypeID DataType="Int32">0</L2AmountTypeID>
                      <L2Cap DataType="Decimal">0.000000</L2Cap>
                      <L3DiscountAmt DataType="Decimal">0.000000</L3DiscountAmt>
                      <L3AmountTypeID DataType="Int32">0</L3AmountTypeID>
                      <ItemLimit DataType="Int32">1</ItemLimit>
                      <WeightLimit DataType="Decimal">0.000000</WeightLimit>
                      <DollarLimit DataType="Decimal">0.000000</DollarLimit>
                      <ChargebackDeptID DataType="Int32">14</ChargebackDeptID>
                      <DecliningBalance DataType="Boolean">false</DecliningBalance>
                      <RetroactiveDiscount DataType="Boolean">false</RetroactiveDiscount>
                      <UserGroupID DataType="Int32">0</UserGroupID>
                      <ChargebackDeptName DataType="String">Tender</ChargebackDeptName>
                      <ChargebackDeptCode DataType="String">0000</ChargebackDeptCode>
                      <PercentFixedRounding DataType="Decimal">0.00</PercentFixedRounding>
                      <Tiers>
                        <Tier>
                          <PKID DataType="Int64">1</PKID>
                          <DiscountID DataType="Int32">1</DiscountID>
                          <TierLevel DataType="Byte">1</TierLevel>
                          <ReceiptDescription DataType="String">offer 1 .05 off</ReceiptDescription>
                          <DiscountAmount DataType="Decimal">0.050000</DiscountAmount>
                          <ItemLimit DataType="Int32">0</ItemLimit>
                          <WeightLimit DataType="Decimal">0.000000</WeightLimit>
                          <DollarLimit DataType="Decimal">0.000000</DollarLimit>
                          <SPRepeatLevel DataType="Int16">0</SPRepeatLevel>
                        </Tier>
                      </Tiers>
                    </Discount>
                  </Rewards>
                  <Auxilary>
                    <CustomerGroup>
                      <Header>
                        <CustomerGroupID>6</CustomerGroupID>
                        <Name>cks test customer group 1</Name>
                        <NewCardholders>false</NewCardholders>
                        <AnyCAMCardholder>false</AnyCAMCardholder>
                        <IsOptInGroup>false</IsOptInGroup>
                      </Header>
                    </CustomerGroup>
                    <LocationGroup>
                      <Header>
                        <LocationGroupID>2</LocationGroupID>
                        <Name>CPE Stores</Name>
                        <Description></Description>
                        <CreatedDate>7/24/2018 8:25:33 AM</CreatedDate>
                        <ExtGroupID></ExtGroupID>
                        <ExtSeqNum></ExtSeqNum>
                        <ExtExcluded>false</ExtExcluded>
                        <AllLocations>false</AllLocations>
                        <LastUpdate>7/24/2018 8:25:46 AM</LastUpdate>
                        <StatusFlag>0</StatusFlag>
                        <TCRMAStatusFlag>0</TCRMAStatusFlag>
                        <EngineID>2</EngineID>
                        <ExcludedLocationGroup>false</ExcludedLocationGroup>
                      </Header>
                      <Locations>
                        <Location>
                          <Header>
                            <LocationID>2</LocationID>
                            <ExtLocationCode>cpe01</ExtLocationCode>
                            <LocationName>cpe01</LocationName>
                            <Address1></Address1>
                            <Address2></Address2>
                            <City></City>
                            <State></State>
                            <Zip></Zip>
                            <TestingLocation>false</TestingLocation>
                            <LastUpdate>7/24/2018 8:25:40 AM</LastUpdate>
                            <StatusFlag>0</StatusFlag>
                            <CountryID>1</CountryID>
                            <ContactName></ContactName>
                            <PhoneNumber></PhoneNumber>
                            <GenIPL>false</GenIPL>
                            <CMOADeployStatus>0</CMOADeployStatus>
                            <EngineID>2</EngineID>
                            <BannerID>0</BannerID>
                          </Header>
                        </Location>
                      </Locations>
                    </LocationGroup>
                    <ProductGroup>
                      <Header>
                        <ProductGroupID>1</ProductGroupID>
                        <Name>Any Product</Name>
                        <AnyProduct>true</AnyProduct>
                      </Header>
                    </ProductGroup>
                    <ProductGroup>
                      <Header>
                        <ProductGroupID>4</ProductGroupID>
                        <Name>cks test product group 1</Name>
                        <AnyProduct>false</AnyProduct>
                      </Header>
                      <Products><![CDATA[00000000000501,1]]></Products>
                    </ProductGroup>
                    <Terminal>
                      <Header>
                        <TerminalTypeID>2</TerminalTypeID>
                        <Name>All CPE Terminals</Name>
                        <Description>All CPE Terminals</Description>
                        <ExtTerminalCode></ExtTerminalCode>
                        <LastUpdate>7/18/2018 3:55:19 PM</LastUpdate>
                        <LayoutID>0</LayoutID>
                        <EngineID>2</EngineID>
                        <SpecificPromosOnly>0</SpecificPromosOnly>
                        <FuelProcessing>false</FuelProcessing>
                        <AnyTerminal>true</AnyTerminal>
                        <BannerID>0</BannerID>
                        <Excluded>false</Excluded>
                      </Header>
                    </Terminal>
                  </Auxilary>
                  <Translations>
                    <OfferTranslations>
                      <Translation>
                        <OfferID DataType="Int64">1</OfferID>
                        <LanguageID DataType="Int32">1</LanguageID>
                        <OfferName DataType="String">ckstest 1</OfferName>
                      </Translation>
                    </OfferTranslations>
                    <DiscountTiersTranslations>
                      <Translation>
                        <DiscountTiersID DataType="Int32">1</DiscountTiersID>
                        <LanguageID DataType="Int32">1</LanguageID>
                        <ReceiptDesc DataType="String">offer 1 .05 off</ReceiptDesc>
                      </Translation>
                    </DiscountTiersTranslations>
                  </Translations>
                </Offer>
            </m_offerXML>
            <m_engineID>2</m_engineID>
          </OfferDefinition>
'''
f = urllib.urlopen("http://153.73.161.9/connectors/CRMOfferConnector.asmx/postOffers?%s" % params)
myResponse = f.read()
print myResponse
f.close()
