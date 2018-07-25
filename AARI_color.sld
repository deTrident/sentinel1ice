<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:se="http://www.opengis.net/se">
  <NamedLayer>
    <se:Name>aari_arc_20170829_pl_a</se:Name>
    <UserStyle>
      <se:Name>aari_arc_20170829_pl_a</se:Name>
      <se:FeatureTypeStyle>
        <se:Rule>
          <se:Name>-9 Open water</se:Name>
          <se:Description>
            <se:Title>-9 Open water</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
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
                    <ogc:Literal>-9</ogc:Literal>
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
                    <ogc:Literal>-9</ogc:Literal>
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
                  <ogc:Literal>-9</ogc:Literal>
                </ogc:PropertyIsEqualTo>
              </ogc:And>
            </ogc:Or>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#27bdff</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>82 Nilas</se:Name>
          <se:Description>
            <se:Title>82 Nilas</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
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
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#004fff</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>83 Young ice</se:Name>
          <se:Description>
            <se:Title>83 Young ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
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
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#f400ff</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>86 First year ice</se:Name>
          <se:Description>
            <se:Title>86 First year ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
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
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#2bbf8d</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>95 Old ice</se:Name>
          <se:Description>
            <se:Title>95 Old ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
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
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#7a0000</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Ice concentration 1/10 - 6/10</se:Name>
          <se:Description>
            <se:Title>Ice concentration 1/10 - 6/10</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
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
              <ogc:PropertyIsEqualTo>
                <ogc:Function name="to_int">
                  <ogc:PropertyName>CT</ogc:PropertyName>
                </ogc:Function>
                <ogc:Literal>40</ogc:Literal>
              </ogc:PropertyIsEqualTo>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#208700</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>Ice concentration 7/10 - 10/10</se:Name>
          <se:Description>
            <se:Title>Ice concentration 7/10 - 10/10</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
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
              <ogc:PropertyIsEqualTo>
                <ogc:Function name="to_int">
                  <ogc:PropertyName>CT</ogc:PropertyName>
                </ogc:Function>
                <ogc:Literal>80</ogc:Literal>
              </ogc:PropertyIsEqualTo>
            </ogc:And>
          </ogc:Filter>
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:SvgParameter name="fill">#f86500</se:SvgParameter>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
        <se:Rule>
          <se:Name>99 Fast ice</se:Name>
          <se:Description>
            <se:Title>99 Fast ice</se:Title>
          </se:Description>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
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
              <ogc:PropertyIsGreaterThan>
                <ogc:Function name="to_int">
                  <ogc:PropertyName>CT</ogc:PropertyName>
                </ogc:Function>
                <ogc:Literal>90</ogc:Literal>
              </ogc:PropertyIsGreaterThan>
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
          <se:PolygonSymbolizer>
            <se:Fill>
              <se:GraphicFill>
                <se:Graphic>
                  <se:Mark>
                    <se:WellKnownName>horline</se:WellKnownName>
                    <se:Stroke>
                      <se:SvgParameter name="stroke">#000000</se:SvgParameter>
                      <se:SvgParameter name="stroke-width">0.5</se:SvgParameter>
                    </se:Stroke>
                  </se:Mark>
                  <se:Size>5</se:Size>
                  <se:Rotation>
                    <ogc:Literal>45</ogc:Literal>
                  </se:Rotation>
                </se:Graphic>
              </se:GraphicFill>
            </se:Fill>
          </se:PolygonSymbolizer>
        </se:Rule>
      </se:FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
