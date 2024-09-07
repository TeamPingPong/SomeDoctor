'use client'

import React, { useState, useMemo, useEffect } from 'react'
import { Radar, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useResultStore } from '@/store/resultStore'


ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
)

interface RadarDataItem {
  description: string;
  status: string;
  value: number;
}

interface RadarData {
  [key: string]: RadarDataItem;
}

interface Participant {
  name: string;
  score: number;
  radarData: RadarData;
  reasoning: string;
}

interface AnalysisData {
  participants: Participant[];
  // categoryDescriptions: {
  //   [key: string]: string;
  // };
  advice: string;
}

interface ColorMap {
  [key: string]: string;
}

export default function Results() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const result = useResultStore((state) => state.result)
  const [participantColors, setParticipantColors] = useState<ColorMap>({})
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  const analysisData: AnalysisData | null = useMemo(() => {
    if (!result) return null
    try {
      if (!result.participants || !Array.isArray(result.participants) || result.participants.length === 0) {
        throw new Error('Invalid or empty participants data')
      }
      // if (typeof result.categoryDescriptions !== 'object' || result.categoryDescriptions === null) {
      //   throw new Error('Invalid categoryDescriptions')
      // }
      if (typeof result.advice !== 'string') {
        throw new Error('Invalid advice')
      }

      result.participants.forEach((participant: Participant, index: number) => {
        if (typeof participant.name !== 'string') {
          throw new Error(`Invalid name for participant at index ${index}`)
        }
        if (typeof participant.score !== 'number') {
          throw new Error(`Invalid score for participant at index ${index}`)
        }
        if (typeof participant.radarData !== 'object' || participant.radarData === null) {
          throw new Error(`Invalid radarData for participant at index ${index}`)
        }
        if (typeof participant.reasoning !== 'string') {
          throw new Error(`Invalid reasoning for participant at index ${index}`)
        }
      })

      return result as AnalysisData
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : String(err)
      setError(`Data format is incorrect: ${errorMessage}. Received: ${JSON.stringify(result, null, 2)}`)
      return null
    }
  }, [result])

  useEffect(() => {
    if (result) {
      setLoading(false)
    }
  }, [result])

  const radarLabels = useMemo(() => {
    if (analysisData?.participants?.[0]?.radarData) {
      return Object.keys(analysisData.participants[0].radarData)
    }
    return []
  }, [analysisData])

  const chartData = useMemo(() => {
    if (!analysisData?.participants) {
      return { labels: [], datasets: [] }
    }

    return {
      labels: radarLabels,
      datasets: analysisData.participants.map((participant: Participant) => {
        const color = participantColors[participant.name] || 'rgb(0, 0, 0)';
        return {
          label: participant.name,
          data: radarLabels.map(label => participant.radarData[label].value),
          backgroundColor: color,
          borderColor: color,
          borderWidth: 1,
        }
      })
    }
  }, [analysisData, radarLabels, participantColors])

  useEffect(() => {
    if (analysisData?.participants) {
      const colors = analysisData.participants.reduce((acc: ColorMap, participant: Participant) => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return {
          ...acc,
          [participant.name]: `rgb(${r}, ${g}, ${b})`
        };
      }, {} as ColorMap);
      setParticipantColors(colors);
    }
  }, [analysisData]);

  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category)
  }

  if (loading) {
    return (
      <div className="container mx-auto mt-10">
        <Card>
          <CardContent>
            <p className="text-center">데이터를 불러오는 중입니다...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto mt-10">
        <Card>
          <CardContent>
            <p className="text-center text-red-500">{error}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!analysisData) {
    return (
      <div className="container mx-auto mt-10">
        <Card>
          <CardContent>
            <p className="text-center">분석 데이터가 없습니다.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto mt-10 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-center">호감도 분석 결과</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap justify-around items-center">
            {analysisData.participants.map((participant: Participant, index: number) => (
              <div key={index} className="text-center p-4">
                <p className="text-2xl font-bold">{participant.score}</p>
                <p>{participant.name}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardContent>
            <Radar 
              data={chartData} 
              options={{
                onClick: (event, elements) => {
                  if (elements.length > 0) {
                    const index = elements[0].index
                    handleCategoryClick(radarLabels[index])
                  }
                },
                plugins: {
                  tooltip: {
                    callbacks: {
                      label: (context) => {
                        return `${context.dataset.label}: ${context.formattedValue}`
                      }
                    }
                  }
                },
                scales: {
                  r: {
                    min: 0,
                    max: 100,
                    ticks: {
                      stepSize: 20
                    }
                  }
                }
              }}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{selectedCategory || '카테고리 설명'}</CardTitle>
          </CardHeader>
          <CardContent>
            {selectedCategory ? (
              <>
                <p className="mb-4">
                  {analysisData.participants[0].radarData[selectedCategory].description}
                </p>
                <Bar 
                  data={{
                    labels: chartData.datasets.map(dataset => dataset.label),
                    datasets: [{
                      label: selectedCategory,
                      data: chartData.datasets.map(dataset => 
                        dataset.data[radarLabels.indexOf(selectedCategory)]
                      ),
                      backgroundColor: chartData.datasets.map(dataset => dataset.backgroundColor),
                      borderColor: chartData.datasets.map(dataset => dataset.borderColor),
                      borderWidth: 1,
                    }]
                  }}
                  options={{
                    responsive: true,
                    indexAxis: 'y',
                    scales: {
                      x: {
                        beginAtZero: true,
                        max: 100
                      }
                    }
                  }}
                />
              </>
            ) : (
              <p>차트에서 카테고리를 선택하세요.</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>참가자별 상세 분석</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {analysisData.participants.map((participant: Participant, index: number) => (
              <div key={index} className="border-b pb-4 last:border-b-0">
                <h3 className="text-lg font-semibold mb-2">{participant.name}</h3>
                <p>{participant.reasoning}</p>
                <div className="mt-2">
                  {Object.entries(participant.radarData).map(([category, data]) => (
                    <div key={category} className="mb-1">
                      <span className="font-medium">{category}:</span> {data.status} ({data.description})
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>전체적인 대화에 대한 조언</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{analysisData.advice}</p>
        </CardContent>
      </Card>
    </div>
  )
}