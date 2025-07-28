import React, { useState } from 'react'
import { StrategyConfig } from '../types'
import { updateStrategyConfig } from '../services/api'
import './StrategyConfigPanel.css'

interface StrategyConfigPanelProps {
  config: StrategyConfig[]
}

const StrategyConfigPanel: React.FC<StrategyConfigPanelProps> = ({ config }) => {
  const [configValues, setConfigValues] = useState<Record<string, string>>(
    config.reduce((acc, item) => ({ ...acc, [item.key]: item.value }), {})
  )
  const [isSaving, setIsSaving] = useState<Record<string, boolean>>({})

  const handleInputChange = (key: string, value: string) => {
    setConfigValues(prev => ({ ...prev, [key]: value }))
  }

  const handleSave = async (key: string) => {
    try {
      setIsSaving(prev => ({ ...prev, [key]: true }))
      await updateStrategyConfig(key, configValues[key])
      setIsSaving(prev => ({ ...prev, [key]: false }))
    } catch (error) {
      console.error(`Error saving ${key}:`, error)
      setIsSaving(prev => ({ ...prev, [key]: false }))
    }
  }

  return (
    <div className="strategy-config-panel">
      <table>
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Value</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {config.map(item => (
            <tr key={item.key}>
              <td>{item.key}</td>
              <td>
                <input
                  type="text"
                  value={configValues[item.key] || ''}
                  onChange={(e) => handleInputChange(item.key, e.target.value)}
                />
              </td>
              <td>
                <button 
                  onClick={() => handleSave(item.key)}
                  disabled={isSaving[item.key]}
                >
                  {isSaving[item.key] ? 'Saving...' : 'Save'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default StrategyConfigPanel
