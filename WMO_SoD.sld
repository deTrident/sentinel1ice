<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>aari_arc_20180424_pl_a</se:Name>
    <UserStyle>
      <se:Name>aari_arc_20180424_pl_a</se:Name>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>Icebergs (S = 98, F = 10)</se:Name>
          <se:Description>
            <se:Title>Icebergs (S = 98, F = 10)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:And>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="max">
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CA</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CB</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CC</ogc:PropertyName>
                          </ogc:Function>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:PropertyIsEqualTo>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>SA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Literal>98</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                    </ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>FA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>10</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:And>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="max">
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CA</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CB</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CC</ogc:PropertyName>
                          </ogc:Function>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:PropertyIsEqualTo>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>SB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Literal>98</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                    </ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>FA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>10</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SC</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>98</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>FA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>10</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PointSymbolizer>
            <se:Graphic>
              <se:Mark>
                <se:WellKnownName>triangle</se:WellKnownName>
                <se:Fill>
                  <se:SvgParameter name="fill">#ff0000</se:SvgParameter>
                </se:Fill>
                <se:Stroke>
                  <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                </se:Stroke>
              </se:Mark>
              <se:Size>11</se:Size>
            </se:Graphic>
          </se:PointSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Undetermined/Unknown (S of the highest C = 99)</se:Name>
          <se:Description>
            <se:Title>Undetermined/Unknown (S of the highest C = 99)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>99</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>99</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>99</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ffffff</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Fast Ice (S = 99, F= 08)</se:Name>
          <se:Description>
            <se:Title>Fast Ice (S = 99, F= 08)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:And>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="max">
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CA</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CB</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CC</ogc:PropertyName>
                          </ogc:Function>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:PropertyIsEqualTo>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>SA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Literal>99</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                    </ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>FA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>8</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:And>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="max">
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CA</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CB</ogc:PropertyName>
                          </ogc:Function>
                          <ogc:Function name="to_int">
                            <ogc:PropertyName>CC</ogc:PropertyName>
                          </ogc:Function>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:PropertyIsEqualTo>
                      <ogc:PropertyIsEqualTo>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>SB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Literal>99</ogc:Literal>
                      </ogc:PropertyIsEqualTo>
                    </ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>FA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>8</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SC</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>99</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>FA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>8</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#969696</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Glacier Ice (S of the highest C = 98)</se:Name>
          <se:Description>
            <se:Title>Glacier Ice (S of the highest C = 98)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>98</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>98</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>98</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#d2d2d2</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Multi-Year Ice (S of the highest C = 97)</se:Name>
          <se:Description>
            <se:Title>Multi-Year Ice (S of the highest C = 97)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>97</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>97</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>97</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#c80000</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Second Year Ice (S of the highest C = 96)</se:Name>
          <se:Description>
            <se:Title>Second Year Ice (S of the highest C = 96)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>96</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>96</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>96</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ff780a</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Old Ice (S of the highest C = 95)</se:Name>
          <se:Description>
            <se:Title>Old Ice (S of the highest C = 95)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>95</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>95</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>95</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#b46432</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Thick First Year Ice (S of the highest C = 93)</se:Name>
          <se:Description>
            <se:Title>Thick First Year Ice (S of the highest C = 93)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>93</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>93</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>93</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#007800</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Medium First Year Ice (S of the highest C = 91)</se:Name>
          <se:Description>
            <se:Title>Medium First Year Ice (S of the highest C = 91)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>91</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>91</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>91</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#00c814</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Thin First Year Stage 2 (S of the highest C = 89)</se:Name>
          <se:Description>
            <se:Title>Thin First Year Stage 2 (S of the highest C = 89)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>89</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>89</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>89</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#affa00</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Thin First Year Stage 1 (S of the highest C = 88)</se:Name>
          <se:Description>
            <se:Title>Thin First Year Stage 1 (S of the highest C = 88)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>88</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>88</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>88</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#d7fa82</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Thin First Year Ice (S of the highest C = 87)</se:Name>
          <se:Description>
            <se:Title>Thin First Year Ice (S of the highest C = 87)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>87</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>87</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>87</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#9bd200</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>First Year Ice (S of the highest C = 86)</se:Name>
          <se:Description>
            <se:Title>First Year Ice (S of the highest C = 86)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>86</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>86</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>86</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ffff00</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Grey - White Ice (S of the highest C = 85)</se:Name>
          <se:Description>
            <se:Title>Grey - White Ice (S of the highest C = 85)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>85</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>85</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>85</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#dc50eb</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Grey Ice (S of the highest C = 84)</se:Name>
          <se:Description>
            <se:Title>Grey Ice (S of the highest C = 84)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>84</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>84</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>84</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#aa28f0</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Young Ice (S of the highest C = 83)</se:Name>
          <se:Description>
            <se:Title>Young Ice (S of the highest C = 83)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>83</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>83</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>83</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ce34ee</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Nilas, Ice Rind (S of the highest C = 82)</se:Name>
          <se:Description>
            <se:Title>Nilas, Ice Rind (S of the highest C = 82)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>82</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>82</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>82</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#ff8aff</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>New ice (S of the highest C = 81)</se:Name>
          <se:Description>
            <se:Title>New ice (S of the highest C = 81)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:Or>
                <ogc:Or>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>81</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                  <ogc:And>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="max">
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CA</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CB</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Function name="to_int">
                          <ogc:PropertyName>CC</ogc:PropertyName>
                        </ogc:Function>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:PropertyIsEqualTo>
                    <ogc:PropertyIsEqualTo>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>SB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Literal>81</ogc:Literal>
                    </ogc:PropertyIsEqualTo>
                  </ogc:And>
                </ogc:Or>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="max">
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CA</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CB</ogc:PropertyName>
                      </ogc:Function>
                      <ogc:Function name="to_int">
                        <ogc:PropertyName>CC</ogc:PropertyName>
                      </ogc:Function>
                    </ogc:Function>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CC</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SC</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>81</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#f0d2fa</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Open water (CT = 01)</se:Name>
          <se:Description>
            <se:Title>Open water (CT = 01)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:PropertyIsEqualTo>
                <ogc:Function name="to_int">
                  <ogc:PropertyName>CT</ogc:PropertyName>
                </ogc:Function>
                <ogc:Literal>1</ogc:Literal>
              </ogc:PropertyIsEqualTo>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#96c8ff</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Ice Free (POLY_TYPE = W)</se:Name>
          <se:Description>
            <se:Title>Ice Free (POLY_TYPE = W)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:Function name="regexp_match">
              <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
              <ogc:Literal>W</ogc:Literal>
            </ogc:Function>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#0064ff</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>AARI Summer Ice Concentration 1/10 - 6/10 (CA = 40, SA = 99, FA = 99)</se:Name>
          <se:Description>
            <se:Title>AARI Summer Ice Concentration 1/10 - 6/10 (CA = 40, SA = 99, FA = 99)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>40</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>99</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>FA</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>99</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#208700</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>AARI Summer Ice Concentration 7/10 - 10/10 (CA = 80, SA = 99, FA = 99)</se:Name>
          <se:Description>
            <se:Title>AARI Summer Ice Concentration 7/10 - 10/10 (CA = 80, SA = 99, FA = 99)</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:Function name="regexp_match">
                <ogc:PropertyName>POLY_TYPE</ogc:PropertyName>
                <ogc:Literal>I</ogc:Literal>
              </ogc:Function>
              <ogc:And>
                <ogc:And>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>CA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>80</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                  <ogc:PropertyIsEqualTo>
                    <ogc:Function name="to_int">
                      <ogc:PropertyName>SA</ogc:PropertyName>
                    </ogc:Function>
                    <ogc:Literal>99</ogc:Literal>
                  </ogc:PropertyIsEqualTo>
                </ogc:And>
                <ogc:PropertyIsEqualTo>
                  <ogc:Function name="to_int">
                    <ogc:PropertyName>FA</ogc:PropertyName>
                  </ogc:Function>
                  <ogc:Literal>99</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#f86500</se:SvgParameter>
            </se:Fill>
            <se:Stroke>
              <se:SvgParameter name="stroke">#000001</se:SvgParameter>
              <se:SvgParameter name="stroke-width">1</se:SvgParameter>
              <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
            </se:Stroke>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
